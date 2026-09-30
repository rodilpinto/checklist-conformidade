#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_v107.py — Gera Checklist Portaria 227/2025 v1.07

Adiciona análise de risco multidimensional:
  Prioridade = Impacto (1-4) × Probabilidade (1-4) + Precedência (0-2)

Faixas:
  P1 (Imediato)    = 20-34
  P2 (Curto prazo) = 12-19
  P3 (Médio prazo) = 6-11
  P4 (Acompanhar)  = 1-5
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from copy import copy
import shutil
import json
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 1. Setup
# ============================================================

src = os.path.join(_ROOT, 'checklists', 'Checklist_Portaria_227_2025_IA_v1.06.xlsx')
dst = os.path.join(_ROOT, 'checklists', 'Checklist_Portaria_227_2025_IA_v1.07.xlsx')
shutil.copy2(src, dst)
print("Copiado v1.06 -> v1.07")

with open(os.path.join(_ROOT, 'data', 'scoring_risco_v107.json'), 'r', encoding='utf-8') as f:
    scoring_list = json.load(f)
scoring = {item['id']: item for item in scoring_list}

with open(os.path.join(_ROOT, 'data', 'checklist_conformidade_data.json'), 'r', encoding='utf-8') as f:
    checklist_data = json.load(f)

wb = openpyxl.load_workbook(dst)

conf_sheet = wb['Checklist Conformidade']
curso_sheet = resumo_sheet = legenda_sheet = None
for s in wb.sheetnames:
    if 'Curso' in s or 'SECIN' in s:
        curso_sheet = wb[s]
    if 'Resumo' in s:
        resumo_sheet = wb[s]
    if 'Legenda' in s:
        legenda_sheet = wb[s]

print(f"Sheets: {wb.sheetnames}")

# ============================================================
# Estilos
# ============================================================

HEADER_FONT = Font(name='Arial', size=11, bold=True, color='FFFFFFFF')
HEADER_FILL = PatternFill('solid', fgColor='FF1F4E79')
HEADER_ALIGN = Alignment(horizontal='center', vertical='top', wrap_text=True)

THIN_BORDER = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin'),
)

DATA_FONT = Font(name='Arial', size=10)
DATA_FONT_BOLD = Font(name='Arial', size=10, bold=True)
DATA_ALIGN_CENTER = Alignment(horizontal='center', vertical='top', wrap_text=True)

P_STYLES = {
    'P1': {
        'fill': PatternFill('solid', fgColor='FFFF0000'),
        'font': Font(name='Arial', size=10, bold=True, color='FFFFFFFF'),
    },
    'P2': {
        'fill': PatternFill('solid', fgColor='FFFF6600'),
        'font': Font(name='Arial', size=10, bold=True, color='FFFFFFFF'),
    },
    'P3': {
        'fill': PatternFill('solid', fgColor='FFFFD700'),
        'font': Font(name='Arial', size=10, bold=True, color='FF000000'),
    },
    'P4': {
        'fill': PatternFill('solid', fgColor='FF00AA00'),
        'font': Font(name='Arial', size=10, bold=True, color='FFFFFFFF'),
    },
}

PRIORITY_LABELS = {
    'P1': 'P1 (Imediato)',
    'P2': 'P2 (Curto prazo)',
    'P3': 'P3 (Médio prazo)',
    'P4': 'P4 (Acompanhar)',
}


def calc_score(s):
    return s['impacto'] * s['probabilidade'] + s['precedencia']


def priority_band(score):
    if score >= 20:
        return 'P1'
    if score >= 12:
        return 'P2'
    if score >= 6:
        return 'P3'
    return 'P4'


def copy_cell_style(src_cell, tgt_cell):
    if src_cell.font:
        tgt_cell.font = copy(src_cell.font)
    if src_cell.alignment:
        tgt_cell.alignment = copy(src_cell.alignment)
    try:
        if src_cell.fill:
            tgt_cell.fill = copy(src_cell.fill)
    except Exception:
        pass
    if src_cell.border:
        tgt_cell.border = copy(src_cell.border)
    if src_cell.number_format:
        tgt_cell.number_format = src_cell.number_format


def snapshot_cell(cell):
    """Read cell value + formatting into a dict."""
    info = {
        'value': cell.value,
        'font': copy(cell.font),
        'alignment': copy(cell.alignment),
        'border': copy(cell.border),
        'number_format': cell.number_format,
    }
    try:
        info['fill'] = copy(cell.fill)
    except Exception:
        info['fill'] = PatternFill()
    return info


def restore_cell(cell, info):
    """Write dict back to cell."""
    cell.value = info['value']
    cell.font = info['font']
    cell.fill = info['fill']
    cell.alignment = info['alignment']
    cell.border = info['border']
    cell.number_format = info['number_format']


def set_header(cell, title):
    cell.value = title
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = HEADER_ALIGN
    cell.border = THIN_BORDER


# ============================================================
# 2. Checklist Conformidade
# ============================================================

print("\n--- Checklist Conformidade ---")

# 2a. Insert 5 new columns after H (col 8) → I..M
#     Existing I-M shift to N-R
conf_sheet.insert_cols(9, 5)
# Layout: A=ID B=Capítulo C=Artigo D=Texto E=Princípio F=Requisito
#         G=Risco H=Nível(v1.06) I=Impacto J=Prob K=Prec L=Score M=Prioridade
#         N=Mitigação O=Responsável P=Evidência Q=Status R=Observações

# 2b. Headers
conf_sheet.cell(row=1, column=8).value = 'Nível de Risco\n(v1.06)'
NEW_HEADERS = {
    9: 'Impacto\n(1-4)',
    10: 'Probabilidade\n(1-4)',
    11: 'Precedência\n(0-2)',
    12: 'Score de\nPrioridade',
    13: 'Prioridade',
}
for col, title in NEW_HEADERS.items():
    set_header(conf_sheet.cell(row=1, column=col), title)

# 2c. Populate scoring data (rows 2-105)
DATA_ROWS_END = 105  # header + 104 items
for row in range(2, DATA_ROWS_END + 1):
    item_id = conf_sheet.cell(row=row, column=1).value
    if item_id is None:
        continue
    item_id = int(item_id)
    if item_id not in scoring:
        continue

    s = scoring[item_id]
    score = calc_score(s)
    band = priority_band(score)

    conf_sheet.cell(row=row, column=9).value = s['impacto']
    conf_sheet.cell(row=row, column=10).value = s['probabilidade']
    conf_sheet.cell(row=row, column=11).value = s['precedencia']
    conf_sheet.cell(row=row, column=12).value = score
    conf_sheet.cell(row=row, column=13).value = PRIORITY_LABELS[band]

    # Estilo colunas numéricas (I, J, K)
    for col in [9, 10, 11]:
        c = conf_sheet.cell(row=row, column=col)
        c.font = DATA_FONT
        c.alignment = DATA_ALIGN_CENTER
        c.border = THIN_BORDER

    # Estilo Score e Prioridade (L, M) com cor da faixa
    ps = P_STYLES[band]
    for col in [12, 13]:
        c = conf_sheet.cell(row=row, column=col)
        c.font = ps['font']
        c.fill = ps['fill']
        c.alignment = DATA_ALIGN_CENTER
        c.border = THIN_BORDER

print(f"  Scoring preenchido para 104 itens")

# 2d. Sort by Score (col L=12) descending
total_cols = conf_sheet.max_column
rows_data = []
for row in range(2, DATA_ROWS_END + 1):
    row_snap = [snapshot_cell(conf_sheet.cell(row=row, column=c))
                for c in range(1, total_cols + 1)]
    rows_data.append(row_snap)

rows_data.sort(key=lambda r: (r[11]['value'] or 0), reverse=True)

for i, row_snap in enumerate(rows_data):
    row = i + 2
    for j, info in enumerate(row_snap):
        restore_cell(conf_sheet.cell(row=row, column=j + 1), info)

print("  Linhas ordenadas por Score (decrescente)")

# 2e. Column widths
conf_sheet.column_dimensions['I'].width = 10
conf_sheet.column_dimensions['J'].width = 15
conf_sheet.column_dimensions['K'].width = 14
conf_sheet.column_dimensions['L'].width = 12
conf_sheet.column_dimensions['M'].width = 22

# ============================================================
# 3. Curso IA Aplicada — SECIN
# ============================================================

if curso_sheet:
    print(f"\n--- {curso_sheet.title} ---")

    # Build article_num → best scoring map
    article_best = {}
    for item in checklist_data:
        m = re.match(r'Art\.\s*(\d+)', item['artigo'])
        if not m:
            continue
        art_num = int(m.group(1))
        s = scoring[item['id']]
        score = calc_score(s)
        if art_num not in article_best or score > article_best[art_num]['score']:
            article_best[art_num] = {
                'impacto': s['impacto'],
                'probabilidade': s['probabilidade'],
                'precedencia': s['precedencia'],
                'score': score,
            }

    def extract_article_nums(text):
        """Extrai números base de artigos de texto de referência."""
        if not text:
            return []
        text = str(text)
        # Remove referências a parágrafos (§1º, §§ 1º-3º, etc.)
        cleaned = re.sub(r'§+\s*\d+[ºª]?', '', text)
        # Remove incisos em algarismo romano
        cleaned = re.sub(r'\b[IVX]+(-[IVX]+)?\b', '', cleaned)
        # Remove palavras-chave
        cleaned = re.sub(r'\b(Pú|caput|Parágrafo)\b', '', cleaned, flags=re.IGNORECASE)
        nums = set()
        # (?<!\d)..(?!\d) instead of \b — "º" (U+00BA) is Unicode \w,
        # so \b doesn't fire between "9" and "º"
        for m_art in re.finditer(r'(?<!\d)(\d{1,2})(?!\d)', cleaned):
            num = int(m_art.group(1))
            if 1 <= num <= 39:
                nums.add(num)
        return sorted(nums)

    # 3a. Insert 5 new columns after H (col 8)
    curso_sheet.insert_cols(9, 5)

    # Headers
    curso_sheet.cell(row=1, column=8).value = 'Nível\n(v1.06)'
    for col, title in NEW_HEADERS.items():
        set_header(curso_sheet.cell(row=1, column=col), title)

    # 3b. Populate scoring via article mapping
    curso_max = curso_sheet.max_row
    mapped = 0
    for row in range(2, curso_max + 1):
        artigos_text = curso_sheet.cell(row=row, column=5).value
        art_nums = extract_article_nums(artigos_text)

        best = None
        for an in art_nums:
            if an in article_best:
                if best is None or article_best[an]['score'] > best['score']:
                    best = article_best[an]

        if not best:
            continue

        score = best['score']
        band = priority_band(score)

        curso_sheet.cell(row=row, column=9).value = best['impacto']
        curso_sheet.cell(row=row, column=10).value = best['probabilidade']
        curso_sheet.cell(row=row, column=11).value = best['precedencia']
        curso_sheet.cell(row=row, column=12).value = score
        curso_sheet.cell(row=row, column=13).value = PRIORITY_LABELS[band]

        for col in [9, 10, 11]:
            c = curso_sheet.cell(row=row, column=col)
            c.font = DATA_FONT
            c.alignment = DATA_ALIGN_CENTER
            c.border = THIN_BORDER

        ps = P_STYLES[band]
        for col in [12, 13]:
            c = curso_sheet.cell(row=row, column=col)
            c.font = ps['font']
            c.fill = ps['fill']
            c.alignment = DATA_ALIGN_CENTER
            c.border = THIN_BORDER

        mapped += 1

    print(f"  Scoring mapeado para {mapped}/{curso_max - 1} itens")

    curso_sheet.column_dimensions['I'].width = 10
    curso_sheet.column_dimensions['J'].width = 15
    curso_sheet.column_dimensions['K'].width = 14
    curso_sheet.column_dimensions['L'].width = 12
    curso_sheet.column_dimensions['M'].width = 22

# ============================================================
# 4. Resumo por Capítulo
# ============================================================

if resumo_sheet:
    print(f"\n--- {resumo_sheet.title} ---")

    # Calculate priority distribution per chapter
    chapter_prio = {}
    for item in checklist_data:
        cap = item['capitulo']
        s = scoring[item['id']]
        score = calc_score(s)
        band = priority_band(score)
        if cap not in chapter_prio:
            chapter_prio[cap] = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
        chapter_prio[cap][band] += 1

    # Insert 4 new columns at D (col 4), shifting old D-G → H-K
    resumo_sheet.insert_cols(4, 4)

    # New headers D-G (P1-P4)
    prio_headers = {
        4: 'P1\n(Imediato)',
        5: 'P2\n(Curto prazo)',
        6: 'P3\n(Médio prazo)',
        7: 'P4\n(Acompanhar)',
    }
    for col, title in prio_headers.items():
        set_header(resumo_sheet.cell(row=1, column=col), title)

    # Rename old headers (now at H-K)
    old_hdr = {8: 'Crítico\n(v1.06)', 9: 'Alto\n(v1.06)',
               10: 'Médio\n(v1.06)', 11: 'Baixo\n(v1.06)'}
    for col, title in old_hdr.items():
        cell = resumo_sheet.cell(row=1, column=col)
        cell.value = title
        # Keep existing header style
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = HEADER_ALIGN
        cell.border = THIN_BORDER

    # Map chapter names from sheet rows to priority data
    # Rows 2-11 = 10 chapters, row 12 = TOTAL
    for row in range(2, 12):
        cap_name = resumo_sheet.cell(row=row, column=1).value
        if not cap_name:
            continue
        cp = chapter_prio.get(str(cap_name), {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0})
        for j, band in enumerate(['P1', 'P2', 'P3', 'P4']):
            c = resumo_sheet.cell(row=row, column=4 + j)
            c.value = cp[band]
            c.font = DATA_FONT
            c.alignment = DATA_ALIGN_CENTER
            c.border = THIN_BORDER

    # TOTAL row (12) — set formulas for ALL numeric columns (D-K)
    # insert_cols doesn't update formula refs, so fix cols H-K too
    for col in range(4, 12):  # D(4) through K(11)
        col_letter = get_column_letter(col)
        c = resumo_sheet.cell(row=12, column=col)
        c.value = f'=SUM({col_letter}2:{col_letter}11)'
        c.font = DATA_FONT_BOLD
        c.alignment = DATA_ALIGN_CENTER
        c.border = THIN_BORDER

    # Column widths
    for col_letter in ['D', 'E', 'F', 'G']:
        resumo_sheet.column_dimensions[col_letter].width = 14

    print("  Atualizado com distribuição P1-P4 por capítulo")

# ============================================================
# 5. Legenda e Instruções
# ============================================================

if legenda_sheet:
    print(f"\n--- {legenda_sheet.title} ---")

    # Update version references
    legenda_sheet.cell(row=1, column=1).value = (
        'CHECKLIST DE CONFORMIDADE — PORTARIA 227/2025 (v1.07)'
    )
    legenda_sheet.cell(row=3, column=1).value = 'Versão 1.07 — 26/02/2026'

    # Add changelog entry
    changelog_row = None
    for row in range(1, legenda_sheet.max_row + 1):
        val = legenda_sheet.cell(row=row, column=1).value
        if val and 'CHANGELOG' in str(val):
            changelog_row = row
            break

    if changelog_row:
        last_entry_row = changelog_row
        for row in range(changelog_row + 1, legenda_sheet.max_row + 1):
            val = legenda_sheet.cell(row=row, column=1).value
            if val and str(val).strip().startswith('v'):
                last_entry_row = row

        new_row = last_entry_row + 1
        # Shift existing content down if there's something below
        legenda_sheet.insert_rows(new_row, 1)
        c = legenda_sheet.cell(row=new_row, column=1)
        c.value = (
            "v1.07 (26/02/2026) — Análise de risco multidimensional: "
            "Impacto × Probabilidade + Precedência; "
            "novas faixas P1–P4; reordenação por prioridade."
        )
        c.font = Font(name='Arial', size=10)
        c.alignment = Alignment(wrap_text=True)

    # Add methodology section at the end
    last_row = legenda_sheet.max_row
    r = last_row + 2

    method = [
        ('METODOLOGIA DE PRIORIZAÇÃO (v1.07)', None, True, False),
        ('Fórmula: Score = Impacto (1-4) × Probabilidade (1-4) + Precedência (0-2)',
         None, False, False),
        ('', '', False, False),
        ('Impacto:',
         '4 = violação legal + dano a pessoas | '
         '3 = vedação expressa / dano institucional | '
         '2 = não conformidade de processo | '
         '1 = lacuna menor', False, True),
        ('Probabilidade:',
         '4 = quase certo (sem controles) | '
         '3 = provável | '
         '2 = possível | '
         '1 = improvável', False, True),
        ('Precedência:',
         '2 = pré-requisito estrutural | '
         '1 = operacional por projeto | '
         '0 = contínuo', False, True),
        ('', '', False, False),
        ('P1 (Imediato):', 'Score 20–34', False, True),
        ('P2 (Curto prazo):', 'Score 12–19', False, True),
        ('P3 (Médio prazo):', 'Score 6–11', False, True),
        ('P4 (Acompanhar):', 'Score 1–5', False, True),
        ('', '', False, False),
        ('Cenário de referência:',
         'órgão público implementando governança de IA pela primeira vez, '
         'sem CETIA constituído, sem processos formais de IA, '
         'uso informal de IA generativa, LGPD parcialmente implementada.',
         False, True),
    ]

    for i, (a, b, is_title, is_label) in enumerate(method):
        row = r + i
        ca = legenda_sheet.cell(row=row, column=1)
        ca.value = a
        if is_title:
            ca.font = Font(name='Arial', size=11, bold=True)
        elif is_label:
            ca.font = Font(name='Arial', size=10, bold=True)
        else:
            ca.font = Font(name='Arial', size=10)
        ca.alignment = Alignment(wrap_text=True)

        if b is not None:
            cb = legenda_sheet.cell(row=row, column=2)
            cb.value = b
            cb.font = Font(name='Arial', size=10)
            cb.alignment = Alignment(wrap_text=True)

    print("  Versão, changelog e metodologia atualizados")

# ============================================================
# 6. Save
# ============================================================

wb.save(dst)
print(f"\nSalvo: {dst}")

# ============================================================
# 7. Sumário
# ============================================================

print("\n" + "=" * 55)
print("DISTRIBUIÇÃO DE PRIORIDADES — v1.07")
print("=" * 55)

totals = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
for item in scoring_list:
    score = calc_score(item)
    totals[priority_band(score)] += 1

for band in ['P1', 'P2', 'P3', 'P4']:
    pct = totals[band] / len(scoring_list) * 100
    bar = '█' * totals[band]
    print(f"  {PRIORITY_LABELS[band]:24s} {totals[band]:3d} ({pct:4.1f}%)  {bar}")
print(f"  {'Total':24s} {sum(totals.values()):3d}")

print("\nComparação com v1.06:")
levels = {'Crítico': 0, 'Alto': 0, 'Médio': 0, 'Baixo': 0}
for item in checklist_data:
    nivel = item.get('nivel', '')
    if nivel in levels:
        levels[nivel] += 1

print("  v1.06: ", end='')
print(' | '.join(f"{k}={v}" for k, v in levels.items()))
print("  v1.07: ", end='')
print(' | '.join(f"{k}={v}" for k, v in totals.items()))

# Top 5
print("\nTop 5 prioridades (maior Score):")
ranked = sorted(scoring_list, key=lambda x: calc_score(x), reverse=True)
for item in ranked[:5]:
    score = calc_score(item)
    cd = next(c for c in checklist_data if c['id'] == item['id'])
    print(f"  ID {item['id']:3d}  Score={score:2d} ({priority_band(score)})  "
          f"{cd['artigo']}  {cd['principio'][:45]}")
