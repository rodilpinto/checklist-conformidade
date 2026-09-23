"""
llm.py -- Integracao com LLMs (Google Gemini ou servidor local OpenAI-compatible)
para geracao de checklists normativos.

Funcoes principais:
    - generate_checklist: envia o texto do normativo ao provider escolhido
      (Gemini ou LLM local) e obtem o checklist em JSON.
    - validate_items: valida, sanitiza e numera os itens retornados pelo LLM.

Uso:
    from lib.llm import generate_checklist, validate_items

    raw_items = generate_checklist(texto_normativo, provider="gemini", api_key="...")
    raw_items = generate_checklist(texto_normativo, provider="local",
                                    base_url="http://<ip-do-servidor>:1234/v1",
                                    model="google/gemma-4")
    items = validate_items(raw_items)

Dependencias:
    - google-genai (provider "gemini")
    - requests (provider "local")
    - lib.prompt_templates (SYSTEM_PROMPT, build_prompt, REQUIRED_FIELDS, VALID_LEVELS)
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, NoReturn

import requests
from google import genai
from google.genai import types

from lib.prompt_templates import (
    REQUIRED_FIELDS,
    VALID_LEVELS,
    build_prompt,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes internas
# ---------------------------------------------------------------------------
_MODEL_NAME: str = "gemini-3.6-flash"

# Tamanho maximo (em caracteres) que enviamos de uma vez ao modelo.
_CHAR_WARN_THRESHOLD: int = 500_000

# Timeout (segundos) para chamadas ao LLM local -- normativos grandes podem
# levar bastante tempo em hardware sem GPU dedicada.
_LOCAL_TIMEOUT_SECONDS: int = 300


# ---------------------------------------------------------------------------
# Erros customizados
# ---------------------------------------------------------------------------
class LLMError(Exception):
    """Erro base para falhas na comunicacao com o LLM."""


class RateLimitError(LLMError):
    """Limite de requisicoes excedido na API do Gemini."""


class TokenLimitError(LLMError):
    """Texto excede o limite de tokens do modelo."""


class JSONParseError(LLMError):
    """Resposta do LLM nao e JSON valido."""


# ---------------------------------------------------------------------------
# Funcao principal: gerar checklist via Gemini
# ---------------------------------------------------------------------------
def generate_checklist(
    text: str,
    api_key: str = "",
    extra_prompt: str = "",
    provider: str = "gemini",
    base_url: str = "",
    model: str = "",
) -> list[dict[str, Any]]:
    """Envia o texto de um normativo ao LLM configurado e retorna o checklist em JSON.

    Args:
        text: Texto integral do normativo (lei, portaria, decreto, etc.).
        api_key: Chave de API do Google Gemini (obrigatoria quando provider="gemini").
        extra_prompt: Instrucoes adicionais do usuario para o LLM (opcional).
        provider: "gemini" (padrao) ou "local" (servidor OpenAI-compatible,
            ex.: LM Studio, na rede interna).
        base_url: URL base do servidor local (obrigatoria quando provider="local"),
            ex.: "http://<ip-do-servidor>:1234/v1".
        model: Nome do modelo no servidor local (obrigatorio quando provider="local"),
            ex.: "google/gemma-4".

    Returns:
        Lista de dicionarios com os itens do checklist (ainda sem validacao
        completa -- use validate_items() em seguida).

    Raises:
        ValueError: Se text ou os parametros obrigatorios do provider estiverem vazios.
        RateLimitError: Se a API retornar erro 429 (limite de requisicoes).
        TokenLimitError: Se o texto exceder o limite do modelo.
        JSONParseError: Se a resposta nao puder ser parseada como JSON.
        LLMError: Para qualquer outro erro na comunicacao com a API.
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

    if provider == "local":
        raw_text = _call_local_llm(text, system_instruction, base_url, model)
    elif provider == "gemini":
        raw_text = _call_gemini(text, system_instruction, api_key)
    else:
        raise ValueError(f"Provider desconhecido: '{provider}'. Use 'gemini' ou 'local'.")

    if not raw_text or not raw_text.strip():
        raise LLMError(
            "O modelo retornou uma resposta vazia. "
            "Tente novamente ou reduza o tamanho do normativo."
        )

    return _parse_json_response(raw_text)


# ---------------------------------------------------------------------------
# Provider: Google Gemini
# ---------------------------------------------------------------------------
def _call_gemini(text: str, system_instruction: str, api_key: str) -> str:
    """Chama a API do Gemini e retorna o texto bruto da resposta."""
    api_key = api_key.strip() if api_key else ""
    if not api_key:
        raise ValueError(
            "A chave de API do Gemini e obrigatoria. "
            "Informe no campo da sidebar ou configure a variavel GEMINI_API_KEY."
        )

    if not api_key.startswith(("AIza", "AQ.")) or len(api_key) < 20:
        raise LLMError(
            "Formato de chave de API invalido. "
            "A chave do Google Gemini deve comecar com 'AIza' ou 'AQ.'. "
            "Verifique sua chave em https://aistudio.google.com/apikey."
        )

    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        temperature=0.1,
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )

    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "").strip() or _MODEL_NAME,
            contents=text,
            config=config,
        )
        return response.text
    except LLMError:
        raise
    except Exception as exc:
        _handle_api_error(exc)


# ---------------------------------------------------------------------------
# Provider: LLM local (servidor OpenAI-compatible, ex.: LM Studio)
# ---------------------------------------------------------------------------
def _call_local_llm(text: str, system_instruction: str, base_url: str, model: str) -> str:
    """Chama um servidor LLM local (API compativel com OpenAI) e retorna o texto bruto."""
    base_url = base_url.strip() if base_url else ""
    model = model.strip() if model else ""

    if not base_url:
        raise ValueError(
            "A URL do servidor LLM local e obrigatoria. "
            "Configure a variavel LOCAL_LLM_URL (ex.: http://<ip-do-servidor>:1234/v1)."
        )
    if not model:
        raise ValueError(
            "O nome do modelo do LLM local e obrigatorio. "
            "Configure a variavel LOCAL_LLM_MODEL (ex.: google/gemma-4)."
        )

    endpoint = base_url.rstrip("/") + "/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": text},
        ],
        "temperature": 0.1,
    }
    if os.getenv("LOCAL_LLM_DISABLE_THINKING", "").strip() == "1":
        payload["chat_template_kwargs"] = {"enable_thinking": False}

    try:
        response = requests.post(endpoint, json=payload, timeout=_LOCAL_TIMEOUT_SECONDS)
    except requests.exceptions.ConnectionError as exc:
        raise LLMError(
            f"Nao foi possivel conectar ao LLM local em '{base_url}'. "
            "Verifique se o servidor esta em execucao e acessivel pela rede "
            "(ex.: precisa estar na rede interna da Camara)."
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise LLMError(
            f"O LLM local em '{base_url}' nao respondeu a tempo "
            f"({_LOCAL_TIMEOUT_SECONDS}s). O normativo pode ser grande demais "
            "para o hardware disponivel; tente reduzi-lo."
        ) from exc

    if response.status_code == 429:
        raise RateLimitError("Limite de requisicoes do LLM local excedido. Aguarde e tente novamente.")
    if response.status_code >= 400:
        raise LLMError(
            f"Erro na comunicacao com o LLM local (HTTP {response.status_code}): "
            f"{response.text[:300]}"
        )

    try:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError) as exc:
        raise JSONParseError(
            "Resposta do LLM local em formato inesperado (nao segue o padrao "
            "OpenAI chat/completions)."
        ) from exc


# ---------------------------------------------------------------------------
# Validacao dos itens retornados
# ---------------------------------------------------------------------------
def validate_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Valida, sanitiza e numera os itens do checklist."""
    if not isinstance(items, list):
        logger.warning("validate_items recebeu tipo %s; convertendo.", type(items))
        items = [items] if isinstance(items, dict) else []

    validated: list[dict[str, Any]] = []
    seq = 0

    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            logger.warning("Item %d ignorado (tipo %s, esperado dict).", idx, type(item))
            continue

        clean = _ensure_required_fields(item)
        clean = _sanitize_string_fields(clean)

        # Normalizar probabilidade e impacto (1-5)
        clean["probabilidade"] = _normalize_score(clean.get("probabilidade"), "probabilidade")
        clean["impacto"] = _normalize_score(clean.get("impacto"), "impacto")

        # Normalizar nivel; se inconsistente com scores, recalcular
        clean["nivel"] = _normalize_level(clean.get("nivel"))
        computed = _compute_nivel_from_scores(clean["probabilidade"], clean["impacto"])
        if computed and clean["nivel"] != computed:
            logger.info(
                "Item %d: nivel '%s' inconsistente com P(%s)xI(%s)=%s. Corrigido para '%s'.",
                idx, clean["nivel"], clean["probabilidade"], clean["impacto"],
                (clean["probabilidade"] or 0) * (clean["impacto"] or 0), computed,
            )
            clean["nivel"] = computed

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


def _handle_api_error(exc: Exception) -> NoReturn:
    """Classifica e relanca excecoes da API com mensagens em portugues."""
    error_msg = str(exc).lower()

    logger.debug("Erro bruto da API Gemini: %s", exc, exc_info=True)

    if "429" in error_msg or "rate limit" in error_msg or "quota" in error_msg:
        raise RateLimitError(
            "Limite de requisicoes da API Gemini excedido. "
            "Aguarde alguns minutos e tente novamente."
        ) from exc

    if any(term in error_msg for term in ("token", "context length", "too long", "max_tokens")):
        raise TokenLimitError(
            "O texto do normativo excede o limite de tokens do modelo. "
            "Divida o normativo em partes menores."
        ) from exc

    if "api key" in error_msg or "api_key_invalid" in error_msg or "401" in error_msg or "403" in error_msg:
        raise LLMError(
            "Chave de API invalida ou expirada. Verifique sua chave "
            "em https://aistudio.google.com/apikey."
        ) from exc

    raise LLMError(
        "Erro na comunicacao com o modelo Gemini. "
        "Verifique sua conexao com a internet e tente novamente."
    ) from exc
