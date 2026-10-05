"""
llm.py -- Geracao de checklists normativos via LLM, pela cadeia de provedores
``llm_cadeia`` (pasta ao lado do app.py; ver llm_cadeia/README.md).

Funcoes principais:
    - generate_checklist: envia o texto do normativo a cadeia de provedores
      (chave do usuario -> LLM local -> Gemini -> Groq -> ...) e obtem o checklist em JSON.
    - validate_items: valida, sanitiza e numera os itens retornados pelo LLM.

Uso:
    from lib.llm import generate_checklist, validate_items

    raw_items, origem = generate_checklist(texto_normativo)
    items = validate_items(raw_items)

Quem responde e decidido pelos segredos (LLM_BASE_URL/LLM_MODEL para o LLM local,
GEMINI_API_KEY, GROQ_API_KEY etc.; tabela em llm_cadeia/README.md) e pela chave
que o usuario digitar na barra lateral (painel_llm).

Dependencias:
    - llm_cadeia (requests; google-genai para os provedores Gemini)
    - lib.prompt_templates (build_prompt, REQUIRED_FIELDS, VALID_LEVELS)
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from llm_cadeia import gerar

from lib.prompt_templates import (
    PAPEIS,
    REQUIRED_FIELDS,
    VALID_LEVELS,
    build_prompt,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes internas
# ---------------------------------------------------------------------------
# Tamanho maximo (em caracteres) que enviamos de uma vez ao modelo.
_CHAR_WARN_THRESHOLD: int = 500_000

_TEMPERATURE: float = 0.1

# Teto de tokens da resposta. Um checklist completo e longo (Portaria 227/2025:
# 91 itens); o llm_cadeia aplica um piso de 4096.
_MAX_TOKENS: int = 32_768


# ---------------------------------------------------------------------------
# Erros customizados
# ---------------------------------------------------------------------------
class LLMError(Exception):
    """Erro base para falhas na comunicacao com o LLM."""


class JSONParseError(LLMError):
    """Resposta do LLM nao e JSON valido."""


# ---------------------------------------------------------------------------
# Funcao principal: gerar checklist pela cadeia de provedores
# ---------------------------------------------------------------------------
def generate_checklist(text: str, extra_prompt: str = "") -> tuple[list[dict[str, Any]], str]:
    """Envia o texto de um normativo a cadeia de LLMs e retorna o checklist em JSON.

    Args:
        text: Texto integral do normativo (lei, portaria, decreto, etc.).
        extra_prompt: Instrucoes adicionais do usuario para o LLM (opcional).

    Returns:
        (itens, origem): lista de dicionarios com os itens do checklist (ainda sem
        validacao completa -- use validate_items() em seguida) e o "provedor (modelo)"
        que respondeu.

    Raises:
        ValueError: Se o texto estiver vazio.
        JSONParseError: Se a resposta nao puder ser parseada como JSON.
        LLMError: Se nenhum provedor responder ou a resposta vier vazia; a mensagem
            lista as tentativas (nunca contem chave).
    """
    if not text or not text.strip():
        raise ValueError("O texto do normativo nao pode estar vazio.")

    if len(text) > _CHAR_WARN_THRESHOLD:
        logger.warning(
            "Texto com %d caracteres. Se a geracao falhar por limite de "
            "tokens, considere dividir o normativo em partes.",
            len(text),
        )

    system_instruction = build_prompt(extra_prompt)

    r = gerar(text, sistema=system_instruction, json=True,
              temperatura=_TEMPERATURE, max_tokens=_MAX_TOKENS)

    if r.texto is None:
        if r.origem:
            raise LLMError(
                f"O modelo {r.origem} retornou uma resposta vazia. "
                "Tente novamente ou reduza o tamanho do normativo."
            )
        tentativas = "\n".join(f"- {t}" for t in r.tentativas) or "- nenhum provedor de IA configurado"
        raise LLMError("Nenhum modelo de IA respondeu. Tentativas:\n\n" + tentativas)

    return _parse_json_response(r.texto), r.origem


# ---------------------------------------------------------------------------
# Validacao dos itens retornados
# ---------------------------------------------------------------------------
def validate_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Valida, sanitiza e numera os itens do checklist.

    Alem dos campos do modelo, cada item sai com:
      - "criticidade": probabilidade x impacto (None sem as duas notas);
      - "nivel": calculado da criticidade (sem notas, o "nivel" do modelo, normalizado);
      - "atores": lista de {"nome", "papel"} sem repeticao, com a mesma grafia
        para o mesmo ator em todos os itens (vale a primeira que aparecer);
      - "responsavel": o ator principal (o 1o "Responsável"; sem nenhum, o 1o ator).
    """
    if not isinstance(items, list):
        logger.warning("validate_items recebeu tipo %s; convertendo.", type(items))
        items = [items] if isinstance(items, dict) else []

    validated: list[dict[str, Any]] = []
    seq = 0
    grafias: dict[str, str] = {}  # nome em minusculas -> 1a grafia vista

    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            logger.warning("Item %d ignorado (tipo %s, esperado dict).", idx, type(item))
            continue

        clean = _ensure_required_fields(item)
        clean = _sanitize_string_fields(clean)

        # Normalizar probabilidade e impacto (1-5)
        clean["probabilidade"] = _normalize_score(clean.get("probabilidade"), "probabilidade")
        clean["impacto"] = _normalize_score(clean.get("impacto"), "impacto")

        # Criticidade e nivel calculados pelo codigo; o "nivel" do modelo so vale sem notas
        p, i = clean["probabilidade"], clean["impacto"]
        clean["criticidade"] = p * i if p is not None and i is not None else None
        clean["nivel"] = (_compute_nivel_from_scores(p, i)
                          or _normalize_level(clean.get("nivel")))

        clean["atores"] = _normalize_atores(clean.get("atores"), clean.get("responsavel"), grafias)
        clean["responsavel"] = _ator_principal(clean["atores"])

        seq += 1
        clean["id"] = seq
        validated.append(clean)

    return validated


# ---------------------------------------------------------------------------
# Funcoes auxiliares privadas
# ---------------------------------------------------------------------------
def _sanitize_string_fields(item: dict[str, Any]) -> dict[str, Any]:
    """Sanitiza campos de texto para prevenir injecao em Excel."""
    _EXCEL_INJECTION_PREFIXES = ("=", "+", "@", "\t", "\r")

    for key, value in item.items():
        if isinstance(value, str):
            stripped = value.strip()
            if stripped and stripped[0] in _EXCEL_INJECTION_PREFIXES:
                stripped = "'" + stripped
            item[key] = stripped
    return item


def _normalize_atores(
    atores: Any, responsavel_texto: Any, grafias: dict[str, str],
) -> list[dict[str, str]]:
    """Lista de atores {"nome", "papel"} limpa, sem repeticao e com grafia unica.

    Sem a lista, aceita o campo antigo "responsavel" em texto ("Ditec / CGE; CDTI"),
    todos com papel "Responsável".
    """
    if not isinstance(atores, list) or not atores:
        texto = str(responsavel_texto or "")
        atores = [{"nome": n, "papel": "Responsável"} for n in re.split(r"[/;]", texto)]

    resultado: list[dict[str, str]] = []
    vistos: set[str] = set()
    for ator in atores:
        if isinstance(ator, str):
            ator = {"nome": ator}
        if not isinstance(ator, dict):
            continue
        nome = re.sub(r"\s+", " ", str(ator.get("nome") or "")).strip()
        if not nome:
            continue
        chave = nome.lower()
        if chave in vistos:
            continue
        vistos.add(chave)
        nome = grafias.setdefault(chave, nome)
        papel = _normalize_papel(ator.get("papel"))
        resultado.append(_sanitize_string_fields({"nome": nome, "papel": papel}))
    return resultado


def _normalize_papel(raw: Any) -> str:
    """'responsavel'/'RESPONSÁVEL' -> 'Responsável'; o resto -> 'Interage'."""
    texto = str(raw or "").strip().lower().replace("á", "a")
    return PAPEIS[0] if texto.startswith("respons") else PAPEIS[1]


def _ator_principal(atores: list[dict[str, str]]) -> str | None:
    for ator in atores:
        if ator["papel"] == PAPEIS[0]:
            return ator["nome"]
    return atores[0]["nome"] if atores else None


def _ensure_required_fields(item: dict[str, Any]) -> dict[str, Any]:
    """Garante que o dicionario contem todos os campos obrigatorios."""
    for field in REQUIRED_FIELDS:
        if field not in item:
            item[field] = None
    return item


def _normalize_level(raw_level: Any) -> str | None:
    """Normaliza o campo 'nivel' para um dos valores validos (MCGR Camara)."""
    if raw_level is None:
        return None

    text = str(raw_level).strip()

    level_map: dict[str, str] = {
        "muito alto": "Muito Alto",
        "alto": "Alto",
        "moderado": "Moderado",
        "medio": "Moderado",
        "médio": "Moderado",
        "baixo": "Baixo",
        # Compatibilidade com termos antigos
        "critico": "Muito Alto",
        "crítico": "Muito Alto",
    }

    normalized = level_map.get(text.lower())
    if normalized:
        return normalized

    logger.warning("Nivel de risco invalido: '%s'. Valores aceitos: %s", text, VALID_LEVELS)
    return None


def _normalize_score(value: Any, field_name: str) -> int | None:
    """Normaliza probabilidade ou impacto para inteiro de 1 a 5."""
    if value is None:
        return None
    try:
        score = int(value)
    except (ValueError, TypeError):
        logger.warning("Valor invalido para %s: '%s'. Esperado inteiro 1-5.", field_name, value)
        return None
    return max(1, min(5, score))


def _compute_nivel_from_scores(prob: int | None, imp: int | None) -> str | None:
    """Calcula o nivel de risco (MCGR) a partir de probabilidade x impacto."""
    if prob is None or imp is None:
        return None
    criticidade = prob * imp
    if criticidade >= 20:
        return "Muito Alto"
    if criticidade >= 10:
        return "Alto"
    if criticidade >= 4:
        return "Moderado"
    return "Baixo"


def _parse_json_response(raw_text: str) -> list[dict[str, Any]]:
    """Tenta parsear a resposta do LLM como JSON."""
    if not raw_text or not raw_text.strip():
        raise JSONParseError(
            "A resposta do modelo veio vazia. "
            "Tente novamente ou verifique se o texto do normativo esta correto."
        )

    text = raw_text.strip()

    # Tentativa 1: parse direto
    try:
        data = json.loads(text)
        return _ensure_list(data)
    except json.JSONDecodeError:
        pass

    # Tentativa 2: extrair JSON de blocos markdown
    md_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if md_match:
        try:
            data = json.loads(md_match.group(1))
            return _ensure_list(data)
        except json.JSONDecodeError:
            pass

    # Tentativa 3: encontrar array JSON
    first_bracket = text.find("[")
    last_bracket = text.rfind("]")
    if first_bracket != -1 and last_bracket > first_bracket:
        try:
            data = json.loads(text[first_bracket : last_bracket + 1])
            return _ensure_list(data)
        except json.JSONDecodeError:
            pass

    raise JSONParseError(
        "Nao foi possivel interpretar a resposta do modelo como JSON. "
        "Tente novamente ou reduza o tamanho do normativo."
    )


def _ensure_list(data: Any) -> list[dict[str, Any]]:
    """Garante que o resultado parseado e uma lista de dicionarios."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("items", "checklist", "data", "results"):
            if key in data and isinstance(data[key], list):
                return data[key]
        return [data]
    raise JSONParseError(
        f"Formato inesperado na resposta do modelo (tipo: {type(data).__name__}). "
        "Esperado: array JSON de objetos."
    )
