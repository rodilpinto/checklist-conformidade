# -*- coding: utf-8 -*-
"""Testes da planilha v1.09 (decisões de 01/10/2026 em _sessao/DECISOES.md):
colunas da v1.08 sem "Nível (v1.06)", ordem por criticidade, sem linhas de capítulo,
abas Checklist / Ações por Ator / Resumo por Capítulo / Legenda, atores separados.

Sem rede: não chama LLM, só validate_items, build_excel e build_prompt.
"""
import sys
from io import BytesIO
from pathlib import Path

import openpyxl
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.excel_builder import build_excel  # noqa: E402
from lib.llm import validate_items  # noqa: E402
from lib.prompt_templates import build_prompt  # noqa: E402


def _bruto(**kw):
    base = {
        "capitulo": "I - Disposições Gerais",
        "artigo": "Art. 1º",
        "texto_literal": "Texto.",
        "principio": "Escopo",
        "requisito": "Req.",
        "risco": "Risco.",
        "probabilidade": 3,
        "impacto": 4,
        "precedencia": "",
        "mitigacao": "Mit.",
        "atores": [{"nome": "Ditec", "papel": "responsavel"}],
        "evidencia": "Ev.",
    }
    base.update(kw)
    return base


def _abrir(items):
    return openpyxl.load_workbook(BytesIO(build_excel(items)))


# ── validate_items ────────────────────────────────────────────────────────────

def test_criticidade_e_nivel_calculados_pelo_codigo():
    [it] = validate_items([_bruto(probabilidade=4, impacto=5, nivel="Baixo")])
    assert it["criticidade"] == 20
    assert it["nivel"] == "Muito Alto"


def test_sem_notas_criticidade_vazia_e_nivel_do_modelo_normalizado():
    [it] = validate_items([_bruto(probabilidade=None, impacto=None, nivel="médio")])
    assert it["criticidade"] is None
    assert it["nivel"] == "Moderado"


def test_atores_normalizados_e_responsavel_principal():
    [it] = validate_items([_bruto(atores=[
        {"nome": " Gestor de Dados ", "papel": "Interage"},
        {"nome": "Encarregado de Proteção de Dados Pessoais", "papel": "RESPONSÁVEL"},
        {"nome": "gestor de dados", "papel": "responsavel"},  # repetido: fica o 1º
        {"nome": "", "papel": "responsavel"},  # vazio: sai
    ])])
    assert it["atores"] == [
        {"nome": "Gestor de Dados", "papel": "Interage"},
        {"nome": "Encarregado de Proteção de Dados Pessoais", "papel": "Responsável"},
    ]
    assert it["responsavel"] == "Encarregado de Proteção de Dados Pessoais"


def test_mesmo_ator_com_grafia_diferente_entre_itens_fica_com_a_primeira():
    itens = validate_items([
        _bruto(atores=[{"nome": "Ditec", "papel": "responsavel"}]),
        _bruto(artigo="Art. 2º", atores=[{"nome": "DITEC", "papel": "responsavel"}]),
    ])
    assert [i["atores"][0]["nome"] for i in itens] == ["Ditec", "Ditec"]


def test_responsavel_em_texto_vira_lista_de_atores():
    """Compatibilidade: modelo que devolve o campo antigo "responsavel" em texto."""
    bruto = _bruto(responsavel="Ditec / Gestor de Negócio; CGE")
    del bruto["atores"]
    [it] = validate_items([bruto])
    assert [a["nome"] for a in it["atores"]] == ["Ditec", "Gestor de Negócio", "CGE"]
    assert all(a["papel"] == "Responsável" for a in it["atores"])
    assert it["responsavel"] == "Ditec"


def test_sem_responsavel_marcado_o_primeiro_ator_e_o_principal():
    [it] = validate_items([_bruto(atores=[{"nome": "CGE", "papel": "interage"}])])
    assert it["responsavel"] == "CGE"


def test_atores_sanitizados_contra_injecao_em_excel():
    [it] = validate_items([_bruto(atores=[{"nome": "=HYPERLINK(1)", "papel": "responsavel"}])])
    assert it["atores"][0]["nome"].startswith("'=")


# ── build_excel ───────────────────────────────────────────────────────────────

CABECALHO_V109 = [
    "ID", "Capítulo", "Artigo(s)", "Texto Literal do Artigo", "Conferência do\nTexto Literal",
    "Princípio / Tema",
    "Requisito / Obrigação", "Risco de Não Conformidade", "Impacto\n(1-5 MCGR)",
    "Probabilidade\n(1-5 MCGR)", "Criticidade\n(I×P)", "Nível de\nRisco MCGR",
    "Precedência\n(decorrências)", "Medida de Mitigação", "Responsável pela Mitigação",
    "Evidência Esperada", "Status", "Observações / Plano de Ação",
]


def _itens_exemplo():
    return validate_items([
        _bruto(artigo="Art. 1º", probabilidade=1, impacto=2,
               atores=[{"nome": "Ditec", "papel": "responsavel"}]),
        _bruto(capitulo="II - Princípios", artigo="Art. 4º", probabilidade=5, impacto=5,
               atores=[{"nome": "Gestor de Dados", "papel": "responsavel"},
                       {"nome": "Ditec", "papel": "interage"}]),
        _bruto(capitulo="II - Princípios", artigo="Art. 5º", probabilidade=3, impacto=4),
    ])


def test_abas_da_v109():
    wb = _abrir(_itens_exemplo())
    assert wb.sheetnames == [
        "Checklist de Conformidade", "Ações por Ator", "Resumo por Capítulo", "Legenda",
    ]


def test_cabecalho_da_aba_principal():
    ws = _abrir(_itens_exemplo()).worksheets[0]
    assert [c.value for c in ws[1]] == CABECALHO_V109


def test_ordenada_pelos_artigos_sem_linhas_de_capitulo():
    """Rodrigo, 06/10: a aba principal na ordem do normativo (antes, por criticidade)."""
    ws = _abrir(_itens_exemplo()).worksheets[0]
    ids = [ws.cell(r, 1).value for r in range(2, ws.max_row + 1)]
    artigos = [ws.cell(r, 3).value for r in range(2, ws.max_row + 1)]
    assert ids == [1, 2, 3]
    assert artigos == ["Art. 1º", "Art. 4º", "Art. 5º"]
    assert ws.max_row == 4  # cabeçalho + 3 itens, nenhuma linha de capítulo


def test_acoes_por_ator_desempata_criticidade_por_impacto_e_depois_por_id():
    itens = validate_items([
        _bruto(artigo="Art. 1º", probabilidade=4, impacto=3),
        _bruto(artigo="Art. 2º", probabilidade=3, impacto=4),
        _bruto(artigo="Art. 3º", probabilidade=4, impacto=3),
        _bruto(artigo="Art. 4º", probabilidade=None, impacto=None),
    ])
    ws = _abrir(itens)["Ações por Ator"]
    assert [ws.cell(r, 3).value for r in range(2, 6)] == [2, 1, 3, 4]


def test_responsavel_da_aba_principal_e_o_ator_principal():
    ws = _abrir(_itens_exemplo()).worksheets[0]
    linha_id2 = next(r for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value == 2)
    assert ws.cell(linha_id2, 15).value == "Gestor de Dados"


def test_acoes_por_ator_uma_linha_por_item_e_ator():
    ws = _abrir(_itens_exemplo())["Ações por Ator"]
    linhas = [[ws.cell(r, c).value for c in range(1, 4)] for r in range(2, ws.max_row + 1)]
    # ordem: ator (alfabética), depois criticidade decrescente
    assert linhas == [
        ["Ditec", "Interage", 2],
        ["Ditec", "Responsável", 3],
        ["Ditec", "Responsável", 1],
        ["Gestor de Dados", "Responsável", 2],
    ]
    assert ws.auto_filter.ref


def test_resumo_por_capitulo_conta_niveis():
    ws = _abrir(_itens_exemplo())["Resumo por Capítulo"]
    cab = [c.value for c in ws[1]]
    assert cab[:3] == ["Capítulo", "Dispositivos", "Total"]
    linhas = {ws.cell(r, 1).value: [ws.cell(r, c).value for c in range(3, 8)]
              for r in range(2, ws.max_row + 1)}
    # Total, Muito Alto, Alto, Moderado, Baixo
    assert linhas["I - Disposições Gerais"] == [1, 0, 0, 0, 1]
    assert linhas["II - Princípios"] == [2, 1, 1, 0, 0]
    assert linhas["Total"] == [3, 1, 1, 0, 1]


def test_status_no_padrao_da_v108():
    ws = _abrir(_itens_exemplo()).worksheets[0]
    formulas = [dv.formula1 for dv in ws.data_validations.dataValidation]
    assert '"Não Iniciado,Em Andamento,Conforme,Não Conforme,Não Aplicável"' in formulas


def test_lista_vazia_continua_dando_erro():
    with pytest.raises(ValueError):
        build_excel([])


# ── prompt ────────────────────────────────────────────────────────────────────

def test_prompt_pede_campos_novos_e_nao_pede_nivel():
    p = build_prompt()
    for campo in ('"principio"', '"precedencia"', '"atores"', '"papel"'):
        assert campo in p
    assert '"nivel"' not in p
    assert '"responsavel":' not in p


def test_prompt_pede_acentos_e_da_exemplos_acentuados():
    """Teste ao vivo de 01/10: com exemplos sem acento, o Gemma devolveu "Gestor de Negocio"."""
    p = build_prompt()
    assert "acentuacao correta" in p
    assert '"Gestor de Negócio"' in p
    assert '"Gestor de Negocio"' not in p
