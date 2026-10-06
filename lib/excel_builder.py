# -*- coding: utf-8 -*-
"""
Gerador de planilha Excel formatada para checklists de conformidade normativa.

Produz um arquivo .xlsx em memória (bytes) pronto para download via Streamlit,
com estilos padronizados, validação de dados, auto-filtro e freeze panes.

Dependências: openpyxl (>= 3.1)

Uso:
    from lib.excel_builder import build_excel

    items = [
        {
            "id": 1,
            "capitulo": "Cap. I",
            "artigo": "Art. 1º",
            "texto_literal": "Texto do dispositivo...",
            "requisito": "Descrição do requisito...",
            "risco": "Descrição do risco...",
            "nivel": "Alto",
            "mitigacao": "Ação de mitigação...",
            "responsavel": "Gestor de Negócio",
            "evidencia": "Documento comprobatório...",
        },
        ...
    ]
    xlsx_bytes = build_excel(items, title="Checklist de Conformidade")
    st.download_button("Baixar Excel", xlsx_bytes, "checklist.xlsx")
"""
from __future__ import annotations

from io import BytesIO
from typing import Any

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.properties import PageSetupProperties
from openpyxl.worksheet.worksheet import Worksheet

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES DE ESTILO
# Padrão visual reutilizado dos scripts create_v106.py e
# create_checklist_roteiro_levantamento.py do projeto.
# ═══════════════════════════════════════════════════════════════════════════════

# -- Fontes -----------------------------------------------------------------
HEADER_FONT = Font(name="Arial", size=11, bold=True, color="FFFFFF")
DATA_FONT = Font(name="Arial", size=10)
DATA_FONT_BOLD = Font(name="Arial", size=10, bold=True)
RISK_FONT_WHITE = Font(name="Arial", size=10, bold=True, color="FFFFFF")
RISK_FONT_DARK = Font(name="Arial", size=10, bold=True, color="000000")

# -- Preenchimentos ----------------------------------------------------------
HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
ALT_ROW_FILL = PatternFill("solid", fgColor="F2F7FB")
WHITE_FILL = PatternFill("solid", fgColor="FFFFFF")

# -- Cores por nível de risco (MCGR - Câmara dos Deputados) -----------------
RISK_FILLS: dict[str, PatternFill] = {
    "Muito Alto": PatternFill("solid", fgColor="FF4444"),   # vermelho
    "Alto": PatternFill("solid", fgColor="FFA500"),          # laranja
    "Moderado": PatternFill("solid", fgColor="FFD700"),      # amarelo
    "Baixo": PatternFill("solid", fgColor="92D050"),         # verde
}

# "Muito Alto" e "Alto" usam fonte branca para contraste sobre fundo
# escuro (vermelho/laranja); "Moderado" e "Baixo" usam fonte escura.
RISK_FONTS: dict[str, Font] = {
    "Muito Alto": RISK_FONT_WHITE,
    "Alto": RISK_FONT_WHITE,
    "Moderado": RISK_FONT_DARK,
    "Baixo": RISK_FONT_DARK,
}

# -- Bordas ------------------------------------------------------------------
THIN_BORDER = Border(
    left=Side(style="thin", color="B4C6E7"),
    right=Side(style="thin", color="B4C6E7"),
    top=Side(style="thin", color="B4C6E7"),
    bottom=Side(style="thin", color="B4C6E7"),
)

# -- Alinhamentos ------------------------------------------------------------
ALIGN_HEADER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_WRAP = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

# -- Layout de colunas -------------------------------------------------------
# (chave do dict, título do header, largura em caracteres)
# Planilha v1.09: colunas da v1.08 da Portaria 227 (gerador-checklists/), menos
# "Nível (v1.06)"; decisão de 01/10/2026 em _sessao/DECISOES.md.
COLUMNS: list[tuple[str, str, int]] = [
    ("id",              "ID",                              5),
    ("capitulo",        "Capítulo",                       16),
    ("artigo",          "Artigo(s)",                      12),
    ("texto_literal",   "Texto Literal do Artigo",        55),
    ("conferencia_literal", "Conferência do\nTexto Literal", 14),
    ("principio",       "Princípio / Tema",               20),
    ("requisito",       "Requisito / Obrigação",          40),
    ("risco",           "Risco de Não Conformidade",      40),
    ("impacto",         "Impacto\n(1-5 MCGR)",            10),
    ("probabilidade",   "Probabilidade\n(1-5 MCGR)",      14),
    ("criticidade",     "Criticidade\n(I×P)",             12),
    ("nivel",           "Nível de\nRisco MCGR",           13),
    ("precedencia",     "Precedência\n(decorrências)",    35),
    ("mitigacao",       "Medida de Mitigação",            40),
    ("responsavel",     "Responsável pela Mitigação",     22),
    ("evidencia",       "Evidência Esperada",             30),
    ("status",          "Status",                         16),
    ("observacoes",     "Observações / Plano de Ação",    30),
]

# Aba "Ações por Ator": uma linha por item × ator
ACOES_COLUMNS: list[tuple[str, str, int]] = [
    ("ator",            "Ator",                           24),
    ("papel",           "Papel",                          13),
    ("id",              "ID do Item",                      8),
    ("capitulo",        "Capítulo",                       16),
    ("artigo",          "Artigo(s)",                      12),
    ("requisito",       "Requisito / Obrigação",          45),
    ("criticidade",     "Criticidade\n(I×P)",             12),
    ("nivel",           "Nível de\nRisco MCGR",           13),
    ("evidencia",       "Evidência Esperada",             35),
    ("status",          "Status",                         16),
    ("observacoes",     "Observações",                    30),
]

# Valores permitidos para validação de dados (Status no padrão da v1.08)
STATUS_OPTIONS = "Não Iniciado,Em Andamento,Conforme,Não Conforme,Não Aplicável"
NIVEL_OPTIONS = "Muito Alto,Alto,Moderado,Baixo"

# Colunas centralizadas (valores curtos)
_CENTER_KEYS = ("id", "conferencia_literal", "probabilidade", "impacto", "criticidade", "nivel",
                "status", "papel")

# Conferência do texto literal (lib/conferencia.py): verde confere, vermelho não confere
CONFERENCIA_STYLES: dict[str, tuple[PatternFill, Font]] = {
    "Confere": (PatternFill("solid", fgColor="C6EFCE"),
                Font(name="Arial", size=10, bold=True, color="006100")),
    "Não confere": (PatternFill("solid", fgColor="FFC7CE"),
                    Font(name="Arial", size=10, bold=True, color="9C0006")),
}

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS INTERNOS
# ═══════════════════════════════════════════════════════════════════════════════


def _style_header_row(ws: Worksheet, row: int, num_cols: int) -> None:
    """Aplica estilo de cabeçalho (azul escuro, fonte branca) a uma linha."""
    for col_idx in range(1, num_cols + 1):
        cell = ws.cell(row=row, column=col_idx)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = ALIGN_HEADER
        cell.border = THIN_BORDER


def _apply_risk_style(cell: Any, nivel: str) -> None:
    """Aplica cor de fundo e fonte ao campo Nível conforme classificação de risco."""
    nivel_normalizado = (nivel or "").strip()
    if nivel_normalizado in RISK_FILLS:
        cell.fill = RISK_FILLS[nivel_normalizado]
        cell.font = RISK_FONTS[nivel_normalizado]


def _auto_fit_row_heights(
    ws: Worksheet,
    header_row: int,
    next_empty_row: int,
    columns: list[tuple[str, str, int]],
) -> None:
    """Ajusta a altura de cada linha proporcionalmente ao texto mais longo.

    Estima quantas linhas visuais o texto ocupa dentro da largura da coluna
    e define a altura da linha de forma que o conteúdo fique visível.
    """
    _CHAR_WIDTH_FACTOR = 0.85  # caracteres por unidade de largura Excel (Arial 10pt)
    _LINE_HEIGHT = 15  # pontos por linha de texto
    _MIN_HEIGHT = 30
    _MAX_HEIGHT = 300
    _HEADER_HEIGHT = 36

    ws.row_dimensions[header_row].height = _HEADER_HEIGHT

    col_widths = [w for (_, _, w) in columns]

    for row_idx in range(header_row + 1, next_empty_row):
        max_lines = 1
        for col_idx, width in enumerate(col_widths, start=1):
            cell = ws.cell(row=row_idx, column=col_idx)
            text = str(cell.value or "")
            if not text:
                continue
            chars_per_line = max(int(width * _CHAR_WIDTH_FACTOR), 1)
            # Conta quebras de linha explícitas + wrapping estimado
            lines = 0
            for paragraph in text.split("\n"):
                lines += max(1, -(-len(paragraph) // chars_per_line))  # ceil division
            max_lines = max(max_lines, lines)

        height = max(_MIN_HEIGHT, min(_MAX_HEIGHT, max_lines * _LINE_HEIGHT))
        ws.row_dimensions[row_idx].height = height


def _build_legend_sheet(wb: Workbook) -> None:
    """Cria a aba 'Legenda' com critérios de risco e aviso sobre IA."""
    ws = wb.create_sheet("Legenda")

    # Larguras
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 70

    row = 1

    # Título
    cell = ws.cell(row=row, column=1, value="Legenda e Critérios de Avaliação")
    cell.font = Font(name="Arial", size=14, bold=True, color="1F4E79")
    cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 36
    row += 2

    # Seção: Metodologia de Gestão de Riscos
    cell = ws.cell(row=row, column=1, value="Metodologia de Gestão de Riscos")
    cell.font = Font(name="Arial", size=12, bold=True, color="1F4E79")
    row += 1

    cell = ws.cell(row=row, column=1, value=(
        "Baseada no Modelo Corporativo de Gestão de Riscos (MCGR) da Câmara dos "
        "Deputados (Ato da Mesa nº 233/2018), que adota referências da ABNT NBR "
        "ISO 31000, COSO-ERM e PMI."
    ))
    cell.font = Font(name="Arial", size=10, italic=True)
    cell.alignment = ALIGN_WRAP
    cell.border = THIN_BORDER
    ws.row_dimensions[row].height = 30
    row += 2

    # Subseção: Escala de Probabilidade
    cell = ws.cell(row=row, column=1, value="Escala de Probabilidade")
    cell.font = Font(name="Arial", size=11, bold=True, color="1F4E79")
    row += 1

    prob_scale = [
        ("5 — Praticamente certo", "Ocorrência quase garantida no prazo associado ao escopo."),
        ("4 — Muito provável", "Repete-se com elevada frequência ou há muitos indícios de que ocorrerá."),
        ("3 — Provável", "Repete-se com frequência razoável ou há indícios de que possa ocorrer."),
        ("2 — Pouco provável", "Histórico aponta para baixa frequência de ocorrência."),
        ("1 — Raro", "Acontece apenas em situações excepcionais; sem histórico conhecido."),
    ]

    for label, desc in prob_scale:
        cell_a = ws.cell(row=row, column=1, value=label)
        cell_a.font = Font(name="Arial", size=10, bold=True)
        cell_a.border = THIN_BORDER
        cell_a.alignment = Alignment(vertical="center")
        cell_b = ws.cell(row=row, column=2, value=desc)
        cell_b.font = Font(name="Arial", size=10)
        cell_b.alignment = ALIGN_WRAP
        cell_b.border = THIN_BORDER
        ws.row_dimensions[row].height = 22
        row += 1

    row += 1

    # Subseção: Escala de Impacto
    cell = ws.cell(row=row, column=1, value="Escala de Impacto")
    cell.font = Font(name="Arial", size=11, bold=True, color="1F4E79")
    row += 1

    impact_scale = [
        ("5 — Muito alto", "Compromete totalmente ou quase totalmente o atingimento do objetivo."),
        ("4 — Alto", "Compromete a maior parte do atingimento do objetivo."),
        ("3 — Médio", "Compromete razoavelmente o atingimento do objetivo."),
        ("2 — Baixo", "Compromete em alguma medida o alcance do objetivo."),
        ("1 — Muito baixo", "Compromete minimamente ou não altera o atingimento do objetivo."),
    ]

    for label, desc in impact_scale:
        cell_a = ws.cell(row=row, column=1, value=label)
        cell_a.font = Font(name="Arial", size=10, bold=True)
        cell_a.border = THIN_BORDER
        cell_a.alignment = Alignment(vertical="center")
        cell_b = ws.cell(row=row, column=2, value=desc)
        cell_b.font = Font(name="Arial", size=10)
        cell_b.alignment = ALIGN_WRAP
        cell_b.border = THIN_BORDER
        ws.row_dimensions[row].height = 22
        row += 1

    row += 1

    # Subseção: Níveis de Risco (Criticidade = Probabilidade × Impacto)
    cell = ws.cell(row=row, column=1, value="Níveis de Risco (Criticidade = P × I)")
    cell.font = Font(name="Arial", size=11, bold=True, color="1F4E79")
    row += 1

    risk_levels = [
        ("Muito Alto", "FF4444", "FFFFFF",
         "Criticidade 20 a 25 — Risco inaceitável que exige tratamento "
         "imediato. Pode comprometer totalmente o atingimento dos objetivos."),
        ("Alto", "FFA500", "FFFFFF",
         "Criticidade 10 a 16 — Risco significativo que demanda ações "
         "prioritárias de tratamento para reduzir a exposição."),
        ("Moderado", "FFD700", "000000",
         "Criticidade 4 a 9 — Risco tolerável sob monitoramento. Pode "
         "exigir ações de mitigação conforme o apetite a riscos definido."),
        ("Baixo", "92D050", "000000",
         "Criticidade 1 a 3 — Risco aceitável. Geralmente aceito sem "
         "necessidade de tratamento adicional."),
    ]

    for nivel, bg_color, fg_color, descricao in risk_levels:
        cell_nivel = ws.cell(row=row, column=1, value=nivel)
        cell_nivel.font = Font(name="Arial", size=11, bold=True, color=fg_color)
        cell_nivel.fill = PatternFill("solid", fgColor=bg_color)
        cell_nivel.alignment = Alignment(horizontal="center", vertical="center")
        cell_nivel.border = THIN_BORDER

        cell_desc = ws.cell(row=row, column=2, value=descricao)
        cell_desc.font = Font(name="Arial", size=10)
        cell_desc.alignment = ALIGN_WRAP
        cell_desc.border = THIN_BORDER
        ws.row_dimensions[row].height = 45
        row += 1

    row += 1

    # Seção: Aviso sobre IA
    cell = ws.cell(row=row, column=1, value="Aviso Importante")
    cell.font = Font(name="Arial", size=12, bold=True, color="CC0000")
    row += 1

    aviso = (
        "Esta planilha foi gerada automaticamente por inteligência artificial "
        "a partir do texto do normativo informado.\n\n"
        "A classificação de risco (Muito Alto, Alto, Moderado, Baixo), os "
        "valores de probabilidade e impacto, a precedência e os atores são "
        "uma SUGESTÃO INICIAL "
        "produzida pela IA com base no teor do dispositivo legal e na "
        "metodologia MCGR da Câmara dos Deputados. Ela NÃO substitui o "
        "julgamento profissional do auditor, gestor ou responsável pela "
        "conformidade.\n\n"
        "É responsabilidade do usuário que gera e utiliza esta planilha:\n"
        "  • Revisar todos os itens e suas classificações;\n"
        "  • Ajustar os níveis de risco conforme o contexto organizacional;\n"
        "  • Validar os requisitos contra o texto original do normativo;\n"
        "  • Complementar ou remover itens conforme necessário.\n\n"
        "A ferramenta é um auxílio para acelerar o trabalho — a decisão "
        "final e a responsabilidade são sempre do profissional."
    )
    cell_aviso = ws.cell(row=row, column=1, value=aviso)
    cell_aviso.font = Font(name="Arial", size=10)
    cell_aviso.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    cell_aviso.border = THIN_BORDER
    ws.row_dimensions[row].height = 200

    row += 2

    # Seção: Campos da planilha
    cell = ws.cell(row=row, column=1, value="Campos da Planilha")
    cell.font = Font(name="Arial", size=12, bold=True, color="1F4E79")
    row += 1

    campos = [
        ("ID", "Número do item, na ordem do normativo (a aba principal segue essa ordem)."),
        ("Capítulo", "Capítulo ou seção do normativo."),
        ("Artigo(s)", "Artigo, inciso, parágrafo ou alínea específica."),
        ("Texto Literal", "Transcrição literal do dispositivo legal (sem paráfrase)."),
        ("Conferência", "Confere: o texto aparece idêntico no normativo (só espaços, aspas e travessões podem variar). Não confere: a ferramenta não o achou no normativo, mesmo depois das rodadas de correção; confira à mão."),
        ("Princípio / Tema", "Princípio ou tema do dispositivo."),
        ("Requisito", "O que deve ser verificado ou atendido."),
        ("Risco", "Consequência do não atendimento ao requisito."),
        ("Impacto", "Impacto sobre os objetivos (1-5, conforme escala MCGR)."),
        ("Probabilidade", "Probabilidade de ocorrência (1-5, conforme escala MCGR)."),
        ("Criticidade", "Impacto × Probabilidade (1 a 25), calculada pela ferramenta."),
        ("Nível MCGR", "Faixa da criticidade: Muito Alto (20-25), Alto (10-16), Moderado (4-9), Baixo (1-3)."),
        ("Precedência", "Dispositivos que decorrem deste ou que ele afeta (informativa; conferir no normativo)."),
        ("Mitigação", "Ação sugerida para atender ao requisito (evitar, transferir, mitigar ou aceitar)."),
        ("Responsável", "Ator principal. Todos os atores do item estão na aba \"Ações por Ator\"."),
        ("Evidência", "Documento ou artefato que comprova o atendimento."),
        ("Status", "Não Iniciado, Em Andamento, Conforme, Não Conforme ou Não Aplicável."),
        ("Observações", "Notas livres do avaliador ou plano de ação."),
        ("Ações por Ator", "Uma linha por item e ator, com o papel (Responsável ou Interage); filtre pelo ator."),
        ("Resumo por Capítulo", "Quantidade de itens por capítulo e nível de risco."),
    ]

    for campo, descricao in campos:
        cell_campo = ws.cell(row=row, column=1, value=campo)
        cell_campo.font = Font(name="Arial", size=10, bold=True)
        cell_campo.border = THIN_BORDER
        cell_campo.alignment = Alignment(vertical="center", wrap_text=True)

        cell_desc = ws.cell(row=row, column=2, value=descricao)
        cell_desc.font = Font(name="Arial", size=10)
        cell_desc.border = THIN_BORDER
        cell_desc.alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[row].height = max(22, 15 * -(-len(descricao) // 75))
        row += 1


def _safe_value(value: Any) -> Any:
    """Retorna valor seguro para célula Excel, tratando None.

    Preserva int/float para que o Excel os reconheça como números;
    converte o restante para string.
    """
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return value
    return str(value)


# ═══════════════════════════════════════════════════════════════════════════════
# ABAS DE TABELA
# ═══════════════════════════════════════════════════════════════════════════════


def _sort_key(item: dict) -> tuple:
    """Criticidade e impacto decrescentes, depois a ordem do normativo (ID).

    Itens sem notas vão para o fim.
    """
    crit = item.get("criticidade")
    imp = item.get("impacto")
    return (
        -(crit if isinstance(crit, (int, float)) else -1),
        -(imp if isinstance(imp, (int, float)) else -1),
        item.get("id") or 0,
    )


def _write_table(
    ws: Worksheet,
    columns: list[tuple[str, str, int]],
    rows: list[dict],
) -> None:
    """Escreve cabeçalho, linhas, filtro, painel fixo, validações e impressão."""
    num_cols = len(columns)
    keys = [key for (key, _, _) in columns]

    for col_idx, (_, header_text, width) in enumerate(columns, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width
        ws.cell(row=1, column=col_idx, value=header_text)
    _style_header_row(ws, 1, num_cols)
    ws.freeze_panes = "A2"

    for row_idx, row in enumerate(rows, start=2):
        row_fill = ALT_ROW_FILL if row_idx % 2 == 1 else WHITE_FILL
        for col_idx, key in enumerate(keys, start=1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.value = _safe_value(row.get(key, ""))
            cell.font = DATA_FONT
            cell.border = THIN_BORDER
            cell.fill = row_fill
            cell.alignment = ALIGN_CENTER if key in _CENTER_KEYS else ALIGN_WRAP
            if key == "nivel":
                _apply_risk_style(cell, str(row.get("nivel", "") or ""))
            elif key == "conferencia_literal" and row.get(key) in CONFERENCIA_STYLES:
                cell.fill, cell.font = CONFERENCIA_STYLES[row[key]]

    last_row = max(len(rows) + 1, 2)
    ws.auto_filter.ref = f"A1:{get_column_letter(num_cols)}{last_row}"

    for key, options, title, error in (
        ("status", STATUS_OPTIONS, "Status", "Selecione um dos status da lista."),
        ("nivel", NIVEL_OPTIONS, "Nível de Risco",
         "Selecione: Muito Alto, Alto, Moderado ou Baixo."),
    ):
        if key not in keys:
            continue
        letter = get_column_letter(keys.index(key) + 1)
        dv = DataValidation(
            type="list",
            formula1=f'"{options}"',
            allow_blank=True,
            showErrorMessage=True,
            errorTitle="Valor inválido",
            error=error,
            showInputMessage=True,
            promptTitle=title,
            prompt=f"Selecione: {options.replace(',', ', ')}.",
        )
        dv.add(f"{letter}2:{letter}{last_row}")
        ws.add_data_validation(dv)

    _auto_fit_row_heights(ws, 1, len(rows) + 2, columns)

    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_A4


def _acoes_rows(items: list[dict]) -> list[dict]:
    """Uma linha por item × ator: ordem alfabética do ator, depois a do checklist."""
    rows = []
    for item in sorted(items, key=_sort_key):
        for ator in item.get("atores") or []:
            rows.append({**item, "ator": ator.get("nome"), "papel": ator.get("papel"),
                         "status": "", "observacoes": ""})
    # sort estável: dentro de cada ator, mantém a ordem do checklist
    rows.sort(key=lambda r: str(r["ator"] or "").casefold())
    return rows


def _build_resumo_sheet(wb: Workbook, items: list[dict]) -> None:
    """Itens por capítulo e nível MCGR, com valores fixos (sem fórmulas)."""
    ws = wb.create_sheet("Resumo por Capítulo")
    niveis = NIVEL_OPTIONS.split(",")
    faixas = {"Muito Alto": "20-25", "Alto": "10-16", "Moderado": "4-9", "Baixo": "1-3"}
    columns = ([("capitulo", "Capítulo", 34), ("dispositivos", "Dispositivos", 26),
                ("total", "Total", 8)]
               + [(n, f"{n}\n({faixas[n]})", 12) for n in niveis])
    if any(item.get("nivel") not in niveis for item in items):
        columns.append(("sem_nivel", "Sem\nclassificação", 14))

    por_capitulo: dict[str, dict] = {}
    for item in sorted(items, key=lambda i: i.get("id") or 0):  # ordem do normativo
        cap = str(item.get("capitulo") or "(sem capítulo)")
        linha = por_capitulo.setdefault(cap, {"capitulo": cap, "artigos": [], "total": 0,
                                              **{n: 0 for n in niveis}, "sem_nivel": 0})
        linha["artigos"].append(str(item.get("artigo") or ""))
        linha["total"] += 1
        nivel = item.get("nivel")
        linha[nivel if nivel in niveis else "sem_nivel"] += 1

    rows = []
    for linha in por_capitulo.values():
        arts = [a for a in linha.pop("artigos") if a]
        if len(arts) > 1 and arts[0] != arts[-1]:
            linha["dispositivos"] = f"{arts[0]} a {arts[-1]}"
        else:
            linha["dispositivos"] = arts[0] if arts else ""
        rows.append(linha)
    total = {"capitulo": "Total", "dispositivos": "",
             **{k: sum(r[k] for r in rows) for k in ["total", *niveis, "sem_nivel"]}}

    for col_idx, (_, header_text, width) in enumerate(columns, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width
        ws.cell(row=1, column=col_idx, value=header_text)
    _style_header_row(ws, 1, len(columns))
    ws.row_dimensions[1].height = 36

    for row_idx, row in enumerate([*rows, total], start=2):
        for col_idx, (key, _, _) in enumerate(columns, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=_safe_value(row.get(key, "")))
            cell.font = DATA_FONT_BOLD if row is total else DATA_FONT
            cell.border = THIN_BORDER
            cell.alignment = ALIGN_WRAP if key in ("capitulo", "dispositivos") else ALIGN_CENTER


# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════


def build_excel(
    items: list[dict],
    title: str = "Checklist de Conformidade",
) -> bytes:
    """
    Gera a planilha v1.09 a partir dos itens validados (``lib.llm.validate_items``).

    Abas: checklist (na ordem do normativo, sem linhas de capítulo), "Ações por
    Ator" (uma linha por item × ator), "Resumo por Capítulo" e "Legenda".

    Parameters
    ----------
    items : list[dict]
        Itens com as chaves de ``COLUMNS`` (id, capitulo, artigo, texto_literal,
        principio, requisito, risco, impacto, probabilidade, criticidade, nivel,
        precedencia, mitigacao, responsavel, evidencia) e ``atores`` (lista de
        {"nome", "papel"}). ``status`` e ``observacoes`` são opcionais.

    title : str
        Título da aba principal (máx. 31 caracteres, limitação Excel).

    Returns
    -------
    bytes
        Conteúdo do arquivo .xlsx pronto para download.

    Raises
    ------
    ValueError
        Se ``items`` estiver vazio.
    """
    if not items:
        raise ValueError("A lista de itens não pode estar vazia.")

    wb = Workbook()
    ws = wb.active

    # Título da aba (Excel limita a 31 caracteres e proíbe \/:*?[])
    safe_title = title
    for ch in ("\\", "/", ":", "*", "?", "[", "]"):
        safe_title = safe_title.replace(ch, "_")
    ws.title = safe_title[:31]

    # Aba principal na ordem do normativo (Rodrigo, 06/10/2026); "Ações por Ator" segue por criticidade
    _write_table(ws, COLUMNS, sorted(items, key=lambda i: i.get("id") or 0))
    _write_table(wb.create_sheet("Ações por Ator"), ACOES_COLUMNS, _acoes_rows(items))
    _build_resumo_sheet(wb, items)
    _build_legend_sheet(wb)

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return buffer.getvalue()
