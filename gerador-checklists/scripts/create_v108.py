#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_v108.py — Gera Checklist Portaria 227/2025 v1.08

Alinha a metodologia de risco ao MCGR (Modelo Corporativo de Gestão de Riscos
da Câmara dos Deputados), conforme Ato da Mesa n. 233/2018.

  Criticidade = Impacto (1-5) × Probabilidade (1-5)

Níveis de risco (MCGR):
  Muito alto  = 20-25 (vermelho)
  Alto        = 10-16 (laranja)
  Moderado    =  4-9  (amarelo)
  Baixo       =  1-3  (verde)

Precedência mantida como coluna informativa (dispositivos em que gera decorrência).
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

src = os.path.join(_ROOT, 'checklists', 'Checklist_Portaria_227_2025_IA_v1.07.xlsx')
dst = os.path.join(_ROOT, 'checklists', 'Checklist_Portaria_227_2025_IA_v1.08.xlsx')
shutil.copy2(src, dst)
print("Copiado v1.07 -> v1.08")

with open(os.path.join(_ROOT, 'data', 'scoring_risco_v108.json'), 'r', encoding='utf-8') as f:
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
DATA_FONT_SMALL = Font(name='Arial', size=9)
DATA_ALIGN_CENTER = Alignment(horizontal='center', vertical='top', wrap_text=True)
DATA_ALIGN_LEFT = Alignment(horizontal='left', vertical='top', wrap_text=True)

# Estilos MCGR — cores do mapa de riscos
NIVEL_STYLES = {
    'Muito alto': {
        'fill': PatternFill('solid', fgColor='FFFF0000'),
        'font': Font(name='Arial', size=10, bold=True, color='FFFFFFFF'),
    },
    'Alto': {
        'fill': PatternFill('solid', fgColor='FFFF6600'),
        'font': Font(name='Arial', size=10, bold=True, color='FFFFFFFF'),
    },
    'Moderado': {
        'fill': PatternFill('solid', fgColor='FFFFD700'),
        'font': Font(name='Arial', size=10, bold=True, color='FF000000'),
    },
    'Baixo': {
        'fill': PatternFill('solid', fgColor='FF00AA00'),
        'font': Font(name='Arial', size=10, bold=True, color='FFFFFFFF'),
    },
}

NIVEL_LABELS = {
    'Muito alto': 'Muito alto (20-25)',
    'Alto': 'Alto (10-16)',
    'Moderado': 'Moderado (4-9)',
    'Baixo': 'Baixo (1-3)',
}


def calc_criticidade(s):
    """Criticidade = Impacto × Probabilidade (MCGR)."""
    return s['impacto'] * s['probabilidade']


def nivel_risco(crit):
    """Nível de risco conforme faixas do MCGR."""
    if crit >= 20:
        return 'Muito alto'
    if crit >= 10:
        return 'Alto'
    if crit >= 4:
        return 'Moderado'
    return 'Baixo'


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
# 2. Checklist Conformidade — Atualizar colunas existentes
# ============================================================
# Layout v1.07 (após insert_cols):
#   A=ID B=Cap C=Art D=Texto E=Princípio F=Req G=Risco
#   H=Nível(v1.06) I=Impacto(1-4) J=Prob(1-4) K=Prec(0-2)
#   L=Score M=Prioridade N=Mitigação O=Resp P=Evidência Q=Status R=Obs
#
# Layout v1.08 (reusa colunas I-M, substitui conteúdo):
#   H=Nível(v1.06) I=Impacto(1-5) J=Prob(1-5) K=Criticidade
#   L=Nível MCGR M=Precedência N=Mitigação ...

print("\n--- Checklist Conformidade ---")

# 2a. Atualizar cabeçalhos
NEW_HEADERS_V108 = {
    9: 'Impacto\n(1-5 MCGR)',
    10: 'Probabilidade\n(1-5 MCGR)',
    11: 'Criticidade\n(I×P)',
    12: 'Nível de\nRisco MCGR',
    13: 'Precedência\n(decorrências)',
}
for col, title in NEW_HEADERS_V108.items():
    set_header(conf_sheet.cell(row=1, column=col), title)

# 2b. Preencher dados (rows 2-105)
DATA_ROWS_END = 105
for row in range(2, DATA_ROWS_END + 1):
    item_id = conf_sheet.cell(row=row, column=1).value
    if item_id is None:
        continue
    item_id = int(item_id)
    if item_id not in scoring:
        continue

    s = scoring[item_id]
    crit = calc_criticidade(s)
    nivel = nivel_risco(crit)
    prec_text = s.get('precedencia', '')

    # I=Impacto, J=Probabilidade
    conf_sheet.cell(row=row, column=9).value = s['impacto']
    conf_sheet.cell(row=row, column=10).value = s['probabilidade']

    # K=Criticidade
    conf_sheet.cell(row=row, column=11).value = crit

    # L=Nível de Risco MCGR
    conf_sheet.cell(row=row, column=12).value = NIVEL_LABELS[nivel]

    # M=Precedência (texto informativo)
    conf_sheet.cell(row=row, column=13).value = prec_text

    # Estilo colunas numéricas (I, J, K)
    for col in [9, 10, 11]:
        c = conf_sheet.cell(row=row, column=col)
        c.font = DATA_FONT
        c.alignment = DATA_ALIGN_CENTER
        c.border = THIN_BORDER

    # Estilo Nível MCGR (L) — cor conforme nível
    ns = NIVEL_STYLES[nivel]
    c = conf_sheet.cell(row=row, column=12)
    c.font = ns['font']
    c.fill = ns['fill']
    c.alignment = DATA_ALIGN_CENTER
    c.border = THIN_BORDER

    # Estilo Precedência (M)
    c = conf_sheet.cell(row=row, column=13)
    c.font = DATA_FONT_SMALL
    c.alignment = DATA_ALIGN_LEFT
    c.border = THIN_BORDER

print(f"  Scoring MCGR preenchido para 104 itens")

# 2c. Reordenar por Criticidade (col K=11) decrescente
total_cols = conf_sheet.max_column
rows_data = []
for row in range(2, DATA_ROWS_END + 1):
    row_snap = [snapshot_cell(conf_sheet.cell(row=row, column=c))
                for c in range(1, total_cols + 1)]
    rows_data.append(row_snap)

# Sort: criticidade (col 11, index 10) desc, then impacto (col 9, index 8) desc
rows_data.sort(key=lambda r: (r[10]['value'] or 0, r[8]['value'] or 0), reverse=True)

for i, row_snap in enumerate(rows_data):
    row = i + 2
    for j, info in enumerate(row_snap):
        restore_cell(conf_sheet.cell(row=row, column=j + 1), info)

print("  Linhas ordenadas por Criticidade (decrescente)")

# 2d. Larguras de coluna
conf_sheet.column_dimensions['I'].width = 10
conf_sheet.column_dimensions['J'].width = 15
conf_sheet.column_dimensions['K'].width = 12
conf_sheet.column_dimensions['L'].width = 22
conf_sheet.column_dimensions['M'].width = 50

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
        crit = calc_criticidade(s)
        if art_num not in article_best or crit > article_best[art_num]['crit']:
            article_best[art_num] = {
                'impacto': s['impacto'],
                'probabilidade': s['probabilidade'],
                'precedencia': s.get('precedencia', ''),
                'crit': crit,
            }

    def extract_article_nums(text):
        """Extrai números base de artigos de texto de referência."""
        if not text:
            return []
        text = str(text)
        cleaned = re.sub(r'§+\s*\d+[ºª]?', '', text)
        cleaned = re.sub(r'\b[IVX]+(-[IVX]+)?\b', '', cleaned)
        cleaned = re.sub(r'\b(Pú|caput|Parágrafo)\b', '', cleaned, flags=re.IGNORECASE)
        nums = set()
        for m_art in re.finditer(r'(?<!\d)(\d{1,2})(?!\d)', cleaned):
            num = int(m_art.group(1))
            if 1 <= num <= 39:
                nums.add(num)
        return sorted(nums)

    # Atualizar cabeçalhos (reusa colunas existentes da v1.07)
    for col, title in NEW_HEADERS_V108.items():
        set_header(curso_sheet.cell(row=1, column=col), title)

    curso_max = curso_sheet.max_row
    mapped = 0
    for row in range(2, curso_max + 1):
        artigos_text = curso_sheet.cell(row=row, column=5).value
        art_nums = extract_article_nums(artigos_text)

        best = None
        for an in art_nums:
            if an in article_best:
                if best is None or article_best[an]['crit'] > best['crit']:
                    best = article_best[an]

        if not best:
            continue

        crit = best['crit']
        nivel = nivel_risco(crit)

        curso_sheet.cell(row=row, column=9).value = best['impacto']
        curso_sheet.cell(row=row, column=10).value = best['probabilidade']
        curso_sheet.cell(row=row, column=11).value = crit
        curso_sheet.cell(row=row, column=12).value = NIVEL_LABELS[nivel]
        curso_sheet.cell(row=row, column=13).value = best.get('precedencia', '')

        for col in [9, 10, 11]:
            c = curso_sheet.cell(row=row, column=col)
            c.font = DATA_FONT
            c.alignment = DATA_ALIGN_CENTER
            c.border = THIN_BORDER

        ns = NIVEL_STYLES[nivel]
        c = curso_sheet.cell(row=row, column=12)
        c.font = ns['font']
        c.fill = ns['fill']
        c.alignment = DATA_ALIGN_CENTER
        c.border = THIN_BORDER

        c = curso_sheet.cell(row=row, column=13)
        c.font = DATA_FONT_SMALL
        c.alignment = DATA_ALIGN_LEFT
        c.border = THIN_BORDER

        mapped += 1

    print(f"  Scoring MCGR mapeado para {mapped}/{curso_max - 1} itens")

    curso_sheet.column_dimensions['I'].width = 10
    curso_sheet.column_dimensions['J'].width = 15
    curso_sheet.column_dimensions['K'].width = 12
    curso_sheet.column_dimensions['L'].width = 22
    curso_sheet.column_dimensions['M'].width = 50

# ============================================================
# 4. Resumo por Capítulo
# ============================================================

if resumo_sheet:
    print(f"\n--- {resumo_sheet.title} ---")

    # Distribuição por nível MCGR e capítulo
    chapter_nivel = {}
    for item in checklist_data:
        cap = item['capitulo']
        s = scoring[item['id']]
        crit = calc_criticidade(s)
        nivel = nivel_risco(crit)
        if cap not in chapter_nivel:
            chapter_nivel[cap] = {'Muito alto': 0, 'Alto': 0, 'Moderado': 0, 'Baixo': 0}
        chapter_nivel[cap][nivel] += 1

    # Atualizar cabeçalhos das colunas D-G (que eram P1-P4 na v1.07)
    nivel_headers = {
        4: 'Muito alto\n(20-25)',
        5: 'Alto\n(10-16)',
        6: 'Moderado\n(4-9)',
        7: 'Baixo\n(1-3)',
    }
    for col, title in nivel_headers.items():
        set_header(resumo_sheet.cell(row=1, column=col), title)

    # Preencher dados — rows 2 a 11
    for row in range(2, 12):
        cap_name = resumo_sheet.cell(row=row, column=1).value
        if not cap_name:
            continue
        cn = chapter_nivel.get(str(cap_name),
                               {'Muito alto': 0, 'Alto': 0, 'Moderado': 0, 'Baixo': 0})
        for j, nivel in enumerate(['Muito alto', 'Alto', 'Moderado', 'Baixo']):
            c = resumo_sheet.cell(row=row, column=4 + j)
            c.value = cn[nivel]
            c.font = DATA_FONT
            c.alignment = DATA_ALIGN_CENTER
            c.border = THIN_BORDER

    # TOTAL row (12)
    for col in range(4, 12):
        col_letter = get_column_letter(col)
        c = resumo_sheet.cell(row=12, column=col)
        c.value = f'=SUM({col_letter}2:{col_letter}11)'
        c.font = DATA_FONT_BOLD
        c.alignment = DATA_ALIGN_CENTER
        c.border = THIN_BORDER

    print("  Atualizado com distribuição Muito alto/Alto/Moderado/Baixo por capítulo")

# ============================================================
# 5. Legenda e Instruções
# ============================================================

if legenda_sheet:
    print(f"\n--- {legenda_sheet.title} ---")

    # Atualizar versão
    legenda_sheet.cell(row=1, column=1).value = (
        'CHECKLIST DE CONFORMIDADE — PORTARIA 227/2025 (v1.08)'
    )
    legenda_sheet.cell(row=3, column=1).value = 'Versão 1.08 — 09/03/2026'

    # Adicionar entrada no changelog
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
        legenda_sheet.insert_rows(new_row, 1)
        c = legenda_sheet.cell(row=new_row, column=1)
        c.value = (
            "v1.08 (09/03/2026) — Alinhamento ao MCGR (Ato da Mesa 233/2018): "
            "escalas 1-5, Criticidade = I×P (1-25), "
            "níveis Baixo/Moderado/Alto/Muito alto; "
            "Precedência como coluna informativa (decorrências)."
        )
        c.font = Font(name='Arial', size=10)
        c.alignment = Alignment(wrap_text=True)

    # Reescrever seção de metodologia
    method_row = None
    for row in range(1, legenda_sheet.max_row + 1):
        val = legenda_sheet.cell(row=row, column=1).value
        if val and 'METODOLOGIA' in str(val):
            method_row = row
            break

    # Limpar linhas da metodologia antiga (até encontrar linha vazia após conteúdo)
    if method_row:
        clear_end = method_row
        for row in range(method_row, legenda_sheet.max_row + 1):
            val_a = legenda_sheet.cell(row=row, column=1).value
            val_b = legenda_sheet.cell(row=row, column=2).value
            if row > method_row and not val_a and not val_b:
                # Pula linhas vazias dentro da metodologia
                next_val = legenda_sheet.cell(row=row + 1, column=1).value
                if not next_val:
                    clear_end = row
                    break
            clear_end = row

        for row in range(method_row, clear_end + 1):
            legenda_sheet.cell(row=row, column=1).value = None
            legenda_sheet.cell(row=row, column=2).value = None
        r = method_row
    else:
        r = legenda_sheet.max_row + 2

    method = [
        ('METODOLOGIA DE AVALIAÇÃO DE RISCOS (v1.08 — MCGR)', None, True, False),
        ('', '', False, False),
        ('Base normativa:', 'Modelo Corporativo de Gestão de Riscos (MCGR) da Câmara dos Deputados, '
         'conforme Ato da Mesa n. 233/2018. '
         'Referências: ISO 31000, COSO-ERM, PMI.', False, True),
        ('', '', False, False),
        ('Fórmula:',
         'Criticidade = Impacto (1-5) × Probabilidade (1-5)', False, True),
        ('Faixa de valores:', '1 a 25', False, True),
        ('', '', False, False),
        ('ESCALA DE IMPACTO (Tabela 4 do MCGR)', None, True, False),
        ('5 — Muito alto:',
         'Compromete totalmente ou quase totalmente o atingimento do objetivo', False, True),
        ('4 — Alto:',
         'Compromete a maior parte do atingimento do objetivo', False, True),
        ('3 — Médio:',
         'Compromete razoavelmente o atingimento do objetivo', False, True),
        ('2 — Baixo:',
         'Compromete em alguma medida o alcance do objetivo', False, True),
        ('1 — Muito baixo:',
         'Compromete minimamente ou não altera o atingimento do objetivo', False, True),
        ('', '', False, False),
        ('ESCALA DE PROBABILIDADE (Tabela 3 do MCGR)', None, True, False),
        ('5 — Praticamente certo:',
         'Ocorrência quase garantida no prazo associado ao escopo', False, True),
        ('4 — Muito provável:',
         'Elevada frequência ou muitos indícios de ocorrência', False, True),
        ('3 — Provável:',
         'Frequência razoável ou indícios de ocorrência', False, True),
        ('2 — Pouco provável:',
         'Baixa frequência de ocorrência', False, True),
        ('1 — Raro:',
         'Situações excepcionais; sem histórico ou indícios', False, True),
        ('', '', False, False),
        ('NÍVEIS DE RISCO (Figura 4 do MCGR)', None, True, False),
        ('Muito alto (vermelho):', 'Criticidade 20 a 25', False, True),
        ('Alto (laranja):', 'Criticidade 10 a 16', False, True),
        ('Moderado (amarelo):', 'Criticidade 4 a 9', False, True),
        ('Baixo (verde):', 'Criticidade 1 a 3', False, True),
        ('', '', False, False),
        ('PRECEDÊNCIA (coluna informativa)',
         'Indica quais outros dispositivos da Portaria 227/2025 e normativos '
         'correlatos são afetados pelo item, evidenciando a cadeia normativa '
         'e o efeito cascata do risco.', False, True),
        ('', '', False, False),
        ('Cenário de referência:',
         'Órgão público implementando governança de IA pela primeira vez, '
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

    print("  Versão, changelog e metodologia MCGR atualizados")

# ============================================================
# 6. Save
# ============================================================

wb.save(dst)
print(f"\nSalvo: {dst}")

# ============================================================
# 7. Sumário
# ============================================================

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("\n" + "=" * 60)
print("DISTRIBUIÇÃO DE NÍVEIS DE RISCO (MCGR) — v1.08")
print("=" * 60)

totals = {'Muito alto': 0, 'Alto': 0, 'Moderado': 0, 'Baixo': 0}
for item in scoring_list:
    crit = calc_criticidade(item)
    totals[nivel_risco(crit)] += 1

for nivel in ['Muito alto', 'Alto', 'Moderado', 'Baixo']:
    pct = totals[nivel] / len(scoring_list) * 100
    bar = '█' * totals[nivel]
    print(f"  {NIVEL_LABELS[nivel]:24s} {totals[nivel]:3d} ({pct:4.1f}%)  {bar}")
print(f"  {'Total':24s} {sum(totals.values()):3d}")

# Comparação v1.07 → v1.08
print("\nComparação com v1.07:")
with open(os.path.join(_ROOT, 'data', 'scoring_risco_v107.json'), 'r', encoding='utf-8') as f:
    scoring_v107 = json.load(f)

old_totals = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
for item in scoring_v107:
    old_score = item['impacto'] * item['probabilidade'] + item['precedencia']
    if old_score >= 20:
        old_totals['P1'] += 1
    elif old_score >= 12:
        old_totals['P2'] += 1
    elif old_score >= 6:
        old_totals['P3'] += 1
    else:
        old_totals['P4'] += 1

print("  v1.07: ", end='')
print(' | '.join(f"{k}={v}" for k, v in old_totals.items()))
print("  v1.08: ", end='')
print(' | '.join(f"{k}={v}" for k, v in totals.items()))

# Mapa de riscos 5×5
print("\nMAPA DE RISCOS (5×5):")
print("         I=1    I=2    I=3    I=4    I=5")
for p in range(5, 0, -1):
    row_str = f"  P={p}  "
    for i in range(1, 6):
        c = p * i
        count = sum(1 for item in scoring_list
                    if item['impacto'] == i and item['probabilidade'] == p)
        if count > 0:
            row_str += f" [{c:2d}:{count:2d}]"
        else:
            row_str += f"  {c:2d}:--"
    print(row_str)

# Top 10
print("\nTop 10 criticidades (maior primeiro):")
ranked = sorted(scoring_list, key=lambda x: calc_criticidade(x), reverse=True)
for item in ranked[:10]:
    crit = calc_criticidade(item)
    cd = next(c for c in checklist_data if c['id'] == item['id'])
    print(f"  ID {item['id']:3d}  Crit={crit:2d} ({nivel_risco(crit):10s})  "
          f"{cd['artigo']}  {cd['principio'][:45]}")
