# -*- coding: utf-8 -*-
"""
conferencia.py -- Confere o texto literal de cada item contra o normativo e,
onde divergir, pede ao modelo novas rodadas até convergir.

Regra (Rodrigo, 06/10/2026): o texto tem de ser literal; havendo divergência,
mais rodadas até a convergência total. O limite de rodadas (``MAX_RODADAS``)
evita laço infinito quando o modelo insiste no erro: o que sobrar sai marcado
"Não confere" na planilha e na tela.

"Confere" = o texto do item aparece idêntico no normativo. A comparação só
tolera espaços e quebras de linha, aspas curvas contra retas, travessões contra
hífens e o espaço antes de pontuação que vem do HTML de alguns portais
("2018 , e"). Letras, acentos e pontuação têm de bater.

Uso:
    from lib.conferencia import convergir
    resumo = convergir(itens, texto, lambda divergentes: corrigir_literais(divergentes, texto))
"""
from __future__ import annotations

import logging
import re
import unicodedata
from typing import Any, Callable

from lib.llm import LLMError

logger = logging.getLogger(__name__)

CONFERE = "Confere"
NAO_CONFERE = "Não confere"

# 📝 Escolha do Claude (06/10/2026), a confirmar pelo Rodrigo
MAX_RODADAS = 3

_ASPAS = str.maketrans({"“": '"', "”": '"', "„": '"', "‘": "'", "’": "'"})


def normalizar(texto: Any) -> str:
    """Forma canônica para comparar: só espaço, aspas e travessões variam."""
    t = unicodedata.normalize("NFC", str(texto or "")).translate(_ASPAS)
    t = re.sub(r"[‐‑‒–—]", "-", t)
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r" ([,.;:)])", r"\1", t)
    return t.strip()


def confere(texto_literal: Any, fonte_normalizada: str) -> bool:
    """True se o texto (normalizado) aparece inteiro no normativo (normalizado)."""
    t = normalizar(texto_literal)
    return bool(t) and t in fonte_normalizada


def convergir(
    itens: list[dict[str, Any]],
    fonte: str,
    corrigir: Callable[[list[dict[str, Any]]], dict[int, str]],
    max_rodadas: int = MAX_RODADAS,
) -> dict[str, Any]:
    """Confere todos os itens e faz rodadas de correção para os divergentes.

    ``corrigir`` recebe os itens divergentes e devolve {id: texto_literal novo}.
    Um texto novo só substitui o antigo se conferir. Cada item ganha
    "conferencia_literal" (CONFERE ou NAO_CONFERE).

    Returns:
        {"total", "rodadas", "corrigidos", "restantes", "erro"}; "erro" é a
        mensagem da falha que interrompeu as rodadas, ou None.
    """
    fonte_normalizada = normalizar(fonte)
    rodadas = corrigidos = 0
    erro = None

    def divergentes() -> list[dict[str, Any]]:
        return [it for it in itens if not confere(it.get("texto_literal"), fonte_normalizada)]

    pendentes = divergentes()
    while pendentes and rodadas < max_rodadas:
        rodadas += 1
        try:
            novos = corrigir(pendentes)
        except (LLMError, ValueError) as exc:
            erro = str(exc)
            logger.warning("Rodada %d de correção do texto literal falhou: %s", rodadas, exc)
            break
        for item in pendentes:
            novo = novos.get(item.get("id"))
            if novo and confere(novo, fonte_normalizada):
                item["texto_literal"] = novo
                corrigidos += 1
        pendentes = divergentes()

    restantes = {id(item) for item in pendentes}
    for item in itens:
        item["conferencia_literal"] = NAO_CONFERE if id(item) in restantes else CONFERE

    return {"total": len(itens), "rodadas": rodadas, "corrigidos": corrigidos,
            "restantes": len(pendentes), "erro": erro}
