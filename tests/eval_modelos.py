"""Avaliacao comparativa de modelos na geracao de checklists (Portaria 227/2025).

Compara a saida do app (generate_checklist + validate_items) com o checklist de
referencia v1.08 (scores de risco sem validacao humana) e com o texto oficial.

Uso (na raiz do repo):
    py tests/eval_modelos.py --modelos gemma,gemini --runs 1 --modo inteiro
    py tests/eval_modelos.py --modelos gemma --modo capitulo

Saida: tests/resultados/<timestamp>/ (relatorio.md, resumo.json, itens_*.json)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env", override=True)

import openpyxl  # noqa: E402

import lib.llm as llm  # noqa: E402

FONTE = ROOT / "tests" / "fixtures" / "portaria_227_2025.txt"
GABARITO = ROOT / "gerador-checklists" / "checklists" / "Checklist_Portaria_227_2025_IA_v1.08.xlsx"
TIMEOUT_APP_SEGUNDOS = 300  # timeout real do app para o LLM local

MODELOS = {
    "gemma": lambda: dict(provider="local", base_url=os.getenv("LOCAL_LLM_URL", ""),
                          model=os.getenv("LOCAL_LLM_MODEL", "")),
    "gemma-norazao": lambda: dict(provider="local", base_url=os.getenv("LOCAL_LLM_URL", ""),
                                  model=os.getenv("LOCAL_LLM_MODEL", "")),
    "gemini": lambda: dict(provider="gemini", api_key=os.getenv("GEMINI_API_KEY", "")),
}

TERMO_OFICIAL = "encarregado de protecao de dados pessoais"


# ---------------------------------------------------------------------------
# Normalizacao e carga
# ---------------------------------------------------------------------------
def norm(texto: str) -> str:
    t = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    t = t.lower().replace("“", '"').replace("”", '"')
    t = re.sub(r"[–—-]", "-", t)
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r" ([,.;:)])", r"\1", t)  # artefato de links no HTML do portal: "2018 , e"
    return t.strip(" .;:")


def carregar_fonte() -> str:
    return FONTE.read_text(encoding="utf-8").split("\n", 1)[1]


def carregar_gabarito() -> list[dict]:
    wb = openpyxl.load_workbook(GABARITO, read_only=True, data_only=True)
    ws = wb["Checklist Conformidade"]
    itens = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or row[3] is None:
            continue
        nivel = str(row[11] or "").split("(")[0].strip().lower()
        itens.append({
            "id": row[0], "capitulo": row[1], "artigo": row[2], "texto_literal": str(row[3]),
            "responsavel": row[14],
            "impacto": int(row[8]) if row[8] else None,
            "probabilidade": int(row[9]) if row[9] else None,
            "nivel": {"muito alto": "Muito Alto", "alto": "Alto", "moderado": "Moderado",
                      "baixo": "Baixo"}.get(nivel),
        })
    return itens


CHARS_POR_TOKEN = 4.1  # medido no Gemma: Portaria 227 = 22.267 chars / 5.384 tokens


def dividir_em_lotes(texto: str, max_tokens: int) -> list[str]:
    """Agrupa artigos consecutivos ate ~max_tokens; cada lote leva o capitulo corrente."""
    unidades = re.split(r"(?m)^(?=CAP[IÍ]TULO |Art\. \d+)", texto)
    artigos, capitulo, pendente = [], "", ""
    for u in unidades:
        if re.match(r"CAP[IÍ]TULO ", u):
            capitulo = " - ".join(l.strip() for l in u.strip().splitlines()[:2])
            pendente += u
        elif re.match(r"Art\. \d+", u):
            artigos.append((capitulo, pendente + u))
            pendente = ""
        else:
            pendente += u  # preambulo
    lotes, atual, cap_lote = [], "", ""
    for cap, art in artigos:
        if atual and (len(atual) + len(art)) / CHARS_POR_TOKEN > max_tokens:
            lotes.append((cap_lote, atual))
            atual = ""
        if not atual:
            cap_lote = cap
        atual += art
    if atual:
        lotes.append((cap_lote, atual))
    return [
        (f"[Trecho do normativo. Capitulo em vigor no inicio do trecho: {cap}]\n\n" if cap
         and not t.lstrip().startswith("CAP") else "") + t
        for cap, t in lotes
    ]


def dividir_por_capitulo(texto: str) -> list[str]:
    partes = re.split(r"(?m)^(?=CAP[IÍ]TULO )", texto)
    preambulo, capitulos = partes[0], partes[1:]
    if not capitulos:
        return [texto]
    capitulos[0] = preambulo + capitulos[0]
    return capitulos


# ---------------------------------------------------------------------------
# Execucao
# ---------------------------------------------------------------------------
def dividir(texto: str, modo: str, lote_tokens: int) -> list[str]:
    if modo == "capitulo":
        return dividir_por_capitulo(texto)
    if modo == "lote":
        return dividir_em_lotes(texto, lote_tokens)
    return [texto]


def executar(nome: str, texto: str, modo: str, lote_tokens: int = 1500) -> dict:
    cfg = MODELOS[nome]()
    os.environ["LOCAL_LLM_DISABLE_THINKING"] = "1" if nome == "gemma-norazao" else ""
    blocos = dividir(texto, modo, lote_tokens)
    itens, erros, tempos, retentativas = [], [], [], 0
    for i, bloco in enumerate(blocos, 1):
        t0 = time.time()
        for tentativa in range(1, 4):
            try:
                itens.extend(llm.generate_checklist(bloco, **cfg))
                break
            except Exception as exc:  # registrar e seguir: robustez e uma das metricas
                causa = f"{exc} | causa: {exc.__cause__}" if exc.__cause__ else str(exc)
                transitorio = re.search(r"503|UNAVAILABLE|high demand|overloaded", causa, re.I)
                if transitorio and tentativa < 3:
                    retentativas += 1
                    time.sleep(30 * tentativa)
                    continue
                erros.append(f"bloco {i}/{len(blocos)}: {type(exc).__name__}: {causa[:400]}")
                break
        tempos.append(time.time() - t0)
    return {
        "itens": llm.validate_items(itens),
        "erros": erros,
        "retentativas": retentativas,
        "blocos": len(blocos),
        "tempo_total_s": round(sum(tempos), 1),
        "tempo_max_bloco_s": round(max(tempos), 1),
    }


# ---------------------------------------------------------------------------
# Metricas
# ---------------------------------------------------------------------------
def casar(gabarito: list[dict], itens: list[dict]) -> list[tuple[dict, dict | None, str]]:
    normas = [norm(it.get("texto_literal")) for it in itens]
    pares = []
    for g in gabarito:
        gn = norm(g["texto_literal"])
        melhor, melhor_r, tipo = None, 0.0, "ausente"
        for it, n in zip(itens, normas):
            if not n:
                continue
            r = SequenceMatcher(None, gn, n, autojunk=False).ratio()
            if r > melhor_r:
                melhor, melhor_r = it, r
        if melhor_r >= 0.85:
            tipo = "casado"
        else:
            for it, n in zip(itens, normas):
                curto, longo = sorted((gn, n), key=len)
                if len(curto) >= 30 and curto in longo:
                    melhor, tipo = it, "contido"
                    break
            else:
                melhor = None
        pares.append((g, melhor, tipo))
    return pares


def fidelidade_literal(itens: list[dict], fonte_norm: str) -> dict:
    exato = quase = outro = vazio = 0
    for it in itens:
        n = norm(it.get("texto_literal"))
        if not n:
            vazio += 1
        elif n in fonte_norm:
            exato += 1
        else:
            m = SequenceMatcher(None, fonte_norm, n, autojunk=False).find_longest_match(
                0, len(fonte_norm), 0, len(n))
            if m.size / len(n) >= 0.9:
                quase += 1
            else:
                outro += 1
    total = max(len(itens), 1)
    return {"exato_pct": round(100 * exato / total, 1), "quase_pct": round(100 * quase / total, 1),
            "divergente_pct": round(100 * outro / total, 1), "vazio": vazio}


def concordancia_risco(pares) -> dict:
    casados = [(g, m) for g, m, t in pares if m is not None]
    if not casados:
        return {"n": 0}
    out = {"n": len(casados)}
    for campo in ("impacto", "probabilidade"):
        vals = [(g[campo], m.get(campo)) for g, m in casados if g[campo] and m.get(campo)]
        if vals:
            out[f"{campo}_exato_pct"] = round(100 * mean(a == b for a, b in vals), 1)
            out[f"{campo}_pm1_pct"] = round(100 * mean(abs(a - b) <= 1 for a, b in vals), 1)
            out[f"{campo}_vies"] = round(mean(b - a for a, b in vals), 2)
    niveis = [(g["nivel"], m.get("nivel")) for g, m in casados if g["nivel"]]
    out["nivel_exato_pct"] = round(100 * mean(a == b for a, b in niveis), 1) if niveis else None
    return out


ATORES = {
    "Ditec": r"ditec|diretoria de inovacao e tecnologia",
    "CETIA": r"cetia|comite de etica no uso da (?:inteligencia|ia\b)",
    "CGE": r"\bcge\b|comite de gestao estrategica",
    "CGSIC": r"cgsic|comite gestor de seguranca da informacao",
    "CDTI": r"cdti|comite diretivo de (?:tic|tecnologia)",
    "Gestor de Negocio": r"gestor(?:es)? de negocio",
    "Gestor de Dados": r"gestor(?:es)? de dados",
    "Encarregado": r"encarregado",
    "Gerente de Projeto": r"gerente(?:s)? de projeto",
    "Usuario": r"usuario",
    "Unidade Administrativa": r"unidades? administrativas?|titular(?:es)? de unidade",
    "Diretor-Geral": r"diretor-geral|diretoria-geral",
}


def atores(texto) -> set[str]:
    t = norm(texto)
    return {nome for nome, rx in ATORES.items() if re.search(rx, t)}


def responsabilidade(pares) -> dict:
    casos = [(atores(g.get("responsavel")), atores(m.get("responsavel"))) for g, m, _ in pares if m]
    casos = [(a, b) for a, b in casos if a]
    if not casos:
        return {"n": 0}
    return {
        "n": len(casos),
        "algum_ator_em_comum_pct": round(100 * mean(bool(a & b) for a, b in casos), 1),
        "jaccard_medio": round(mean(len(a & b) / len(a | b) if b else 0 for a, b in casos), 2),
        "sem_ator_reconhecido": sum(not b for _, b in casos),
    }


def granularidade(gabarito: list[dict], itens: list[dict]) -> dict:
    def por_artigo(lista):
        c = {}
        for it in lista:
            m = re.search(r"art\.?\s*(\d+)", norm(it.get("artigo")))
            if m:
                c[int(m.group(1))] = c.get(int(m.group(1)), 0) + 1
        return c
    g, m = por_artigo(gabarito), por_artigo(itens)
    arts = sorted(set(g) | set(m))
    return {
        "artigos": len(arts),
        "mesma_contagem_pct": round(100 * mean(g.get(a, 0) == m.get(a, 0) for a in arts), 1),
        "artigos_com_mais_itens": sum(m.get(a, 0) > g.get(a, 0) for a in arts),
        "artigos_com_menos_itens": sum(m.get(a, 0) < g.get(a, 0) for a in arts),
    }


def terminologia(itens: list[dict]) -> dict:
    textos = " || ".join(norm(v) for it in itens for v in it.values() if isinstance(v, str))
    return {
        "oficial": textos.count(TERMO_OFICIAL),
        "nao_oficial": len(re.findall(r"encarregado de dados pessoais", textos)),
        "dpo": len(re.findall(r"\bdpo\b", textos)),
    }


def avaliar(resultado: dict, gabarito: list[dict], fonte_norm: str) -> dict:
    itens = resultado["itens"]
    pares = casar(gabarito, itens)
    cobertos = sum(t != "ausente" for _, _, t in pares)
    usados = {id(m) for _, m, _ in pares if m is not None}
    return {
        "sucesso": not resultado["erros"],
        "erros": resultado["erros"],
        "retentativas": resultado.get("retentativas", 0),
        "n_itens": len(itens),
        "tempo_total_s": resultado["tempo_total_s"],
        "tempo_max_bloco_s": resultado["tempo_max_bloco_s"],
        "estouraria_timeout_app": resultado["tempo_max_bloco_s"] > TIMEOUT_APP_SEGUNDOS,
        "cobertura_pct": round(100 * cobertos / len(gabarito), 1),
        "cobertura_contido": sum(t == "contido" for _, _, t in pares),
        "itens_sem_par_no_gabarito": sum(id(it) not in usados for it in itens),
        "fidelidade": fidelidade_literal(itens, fonte_norm),
        "responsabilidade": responsabilidade(pares),
        "granularidade": granularidade(gabarito, itens),
        "risco": concordancia_risco(pares),
        "terminologia": terminologia(itens),
    }


# ---------------------------------------------------------------------------
# Relatorio
# ---------------------------------------------------------------------------
def relatorio(resumo: dict, ref: dict) -> str:
    linhas = [
        f"# Avaliacao de modelos: Portaria 227/2025 ({resumo['inicio']})",
        "",
        f"Gabarito: v1.08, {ref['n_gabarito']} itens. Fonte: texto oficial ({ref['chars_fonte']} caracteres).",
        f"Referencia de fidelidade do proprio gabarito: {ref['fidelidade_gabarito']}",
        "",
        "| Modelo | Modo | Run | OK | Itens | Tempo (s) | Maior bloco (s) | Cobertura | Literal exato | "
        "Granularidade | Resp.: ator em comum | Sem par | DPO | Nivel exato |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in resumo["execucoes"]:
        a = r["avaliacao"]
        rk, rp, gr = a["risco"], a.get("responsabilidade", {}), a.get("granularidade", {})
        linhas.append(
            f"| {r['modelo']} | {r['modo']} | {r['run']} | {'sim' if a['sucesso'] else 'NAO'} | "
            f"{a['n_itens']} | {a['tempo_total_s']} | {a['tempo_max_bloco_s']}"
            f"{' (!)' if a['estouraria_timeout_app'] else ''} | "
            f"{a['cobertura_pct']}% | {a['fidelidade']['exato_pct']}% | "
            f"{gr.get('mesma_contagem_pct', '-')}% | {rp.get('algum_ator_em_comum_pct', '-')}% | "
            f"{a['itens_sem_par_no_gabarito']} | {a['terminologia']['dpo']} | {rk.get('nivel_exato_pct', '-')}% |"
        )
    linhas += ["", "(!) = algum bloco levou mais que o timeout do app (300 s).", "", "## Erros"]
    for r in resumo["execucoes"]:
        for e in r["avaliacao"]["erros"]:
            linhas.append(f"- {r['modelo']}/{r['modo']}/run{r['run']}: {e[:300]}")
    return "\n".join(linhas) + "\n"


def exportar_lotes(pasta: Path, lote_tokens: int) -> None:
    from lib.prompt_templates import build_prompt
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "prompt_sistema.txt").write_text(build_prompt(""), encoding="utf-8")
    lotes = dividir_em_lotes(carregar_fonte(), lote_tokens)
    for i, lote in enumerate(lotes, 1):
        (pasta / f"lote_{i:02d}.txt").write_text(lote, encoding="utf-8")
    print(f"{len(lotes)} lotes de ate ~{lote_tokens} tokens em {pasta}")


def importar(pasta: Path, nome: str, lote_tokens: int) -> None:
    fonte_norm, gabarito = norm(carregar_fonte()), carregar_gabarito()
    brutos, erros = [], []
    n_lotes = len(list(pasta.glob("lote_*.txt")))
    for i in range(1, n_lotes + 1):
        arq = pasta / f"lote_{i:02d}.json"
        try:
            brutos.extend(llm._parse_json_response(arq.read_text(encoding="utf-8")))
        except Exception as exc:
            erros.append(f"lote {i}: {type(exc).__name__}: {exc}")
    res = {"itens": llm.validate_items(brutos), "erros": erros, "tempo_total_s": 0, "tempo_max_bloco_s": 0}
    av = avaliar(res, gabarito, fonte_norm)
    saida = ROOT / "tests" / "resultados" / f"{datetime.now():%Y%m%d_%H%M%S}_{nome}"
    saida.mkdir(parents=True, exist_ok=True)
    modo = f"lote{lote_tokens}"
    (saida / f"itens_{nome}_{modo}_run1.json").write_text(
        json.dumps(res["itens"], ensure_ascii=False, indent=1), encoding="utf-8")
    ref = {"n_gabarito": len(gabarito), "chars_fonte": len(fonte_norm),
           "fidelidade_gabarito": fidelidade_literal(gabarito, fonte_norm)}
    resumo = {"inicio": saida.name, "referencia": ref,
              "execucoes": [{"modelo": nome, "modo": modo, "run": 1, "avaliacao": av}]}
    (saida / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    (saida / "relatorio.md").write_text(relatorio(resumo, ref), encoding="utf-8")
    print(f"{nome}: itens={av['n_itens']} cobertura={av['cobertura_pct']}% erros={len(erros)} -> {saida}")


def reavaliar(pasta: Path) -> None:
    fonte_norm = norm(carregar_fonte())
    gabarito = carregar_gabarito()
    resumo = json.loads((pasta / "resumo.json").read_text(encoding="utf-8"))
    resumo["referencia"]["fidelidade_gabarito"] = fidelidade_literal(gabarito, fonte_norm)
    for ex in resumo["execucoes"]:
        arq = pasta / f"itens_{ex['modelo']}_{ex['modo']}_run{ex['run']}.json"
        itens = json.loads(arq.read_text(encoding="utf-8"))
        antigo = ex["avaliacao"]
        res = {"itens": itens, "erros": antigo["erros"], "tempo_total_s": antigo["tempo_total_s"],
               "tempo_max_bloco_s": antigo["tempo_max_bloco_s"]}
        ex["avaliacao"] = avaliar(res, gabarito, fonte_norm)
    (pasta / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    (pasta / "relatorio.md").write_text(relatorio(resumo, resumo["referencia"]), encoding="utf-8")
    print(f"Reavaliado: {pasta / 'relatorio.md'}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelos", default="gemma,gemini")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--modo", choices=["inteiro", "capitulo", "lote"], default="inteiro")
    ap.add_argument("--lote-tokens", type=int, default=1500)
    ap.add_argument("--reavaliar", help="pasta de resultados: recalcula metricas sem chamar modelos")
    ap.add_argument("--exportar-lotes", help="grava lote_XX.txt e prompt_sistema.txt nesta pasta")
    ap.add_argument("--importar", help="pasta com lote_XX.json gerados fora do app (ex.: subagentes)")
    ap.add_argument("--nome", help="nome do modelo para --importar")
    args = ap.parse_args()
    if args.reavaliar:
        reavaliar(Path(args.reavaliar))
        return
    if args.exportar_lotes:
        exportar_lotes(Path(args.exportar_lotes), args.lote_tokens)
        return
    if args.importar:
        importar(Path(args.importar), args.nome, args.lote_tokens)
        return

    llm._LOCAL_TIMEOUT_SECONDS = 1800  # medir o tempo real em vez de cortar no timeout do app
    fonte = carregar_fonte()
    fonte_norm = norm(fonte)
    gabarito = carregar_gabarito()
    ref = {
        "n_gabarito": len(gabarito),
        "chars_fonte": len(fonte),
        "fidelidade_gabarito": fidelidade_literal(gabarito, fonte_norm),
    }

    inicio = datetime.now().strftime("%Y%m%d_%H%M%S")
    saida = ROOT / "tests" / "resultados" / inicio
    saida.mkdir(parents=True, exist_ok=True)
    resumo = {"inicio": inicio, "referencia": ref, "execucoes": []}

    for nome in args.modelos.split(","):
        for run in range(1, args.runs + 1):
            modo = f"lote{args.lote_tokens}" if args.modo == "lote" else args.modo
            print(f"[{datetime.now():%H:%M:%S}] {nome} / {modo} / run {run}...", flush=True)
            res = executar(nome, fonte, args.modo, args.lote_tokens)
            av = avaliar(res, gabarito, fonte_norm)
            (saida / f"itens_{nome}_{modo}_run{run}.json").write_text(
                json.dumps(res["itens"], ensure_ascii=False, indent=1), encoding="utf-8")
            resumo["execucoes"].append({"modelo": nome, "modo": modo, "run": run, "avaliacao": av})
            print(f"    itens={av['n_itens']} cobertura={av['cobertura_pct']}% "
                  f"tempo={av['tempo_total_s']}s erros={len(av['erros'])}", flush=True)
            (saida / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1),
                                               encoding="utf-8")

    (saida / "relatorio.md").write_text(relatorio(resumo, ref), encoding="utf-8")
    print(f"\nRelatorio: {saida / 'relatorio.md'}")


if __name__ == "__main__":
    main()
