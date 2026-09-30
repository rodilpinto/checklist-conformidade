# -*- coding: utf-8 -*-
"""
create_docs_operacionais.py
Gera os 14 documentos operacionais da Portaria 227/2025.

Uso:
    python create_docs_operacionais.py

Saída:
    docs_operacionais/DOC-01_*.xlsx ... DOC-14_*.xlsx/.docx
"""
import os
import sys
import time

# Garantir encoding UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from docs_lote1 import create_doc01, create_doc02, create_doc05
from docs_lote2 import create_doc03, create_doc06, create_doc12
from docs_lote3 import create_doc04, create_doc07, create_doc10, create_doc11
from docs_lote4 import create_doc08, create_doc09, create_doc13, create_doc14


def main():
    start = time.time()

    print("=" * 70)
    print("GERAÇÃO DE DOCUMENTOS OPERACIONAIS — PORTARIA 227/2025")
    print("Política de Governança de IA — Câmara dos Deputados")
    print("=" * 70)
    print()

    docs = [
        ("LOTE 1 — Formulários", [
            create_doc01,   # Formulário de Solicitação e Autorização de Acesso a Dados
            create_doc02,   # Formulário de Avaliação de Riscos Éticos de IA
            create_doc05,   # Mapeamento e Classificação de Dados
        ]),
        ("LOTE 2 — Matrizes e Inventários", [
            create_doc03,   # Matriz RACI de Governança de IA
            create_doc06,   # Glossário Oficial de IA
            create_doc12,   # Inventário de Dados Restritos
        ]),
        ("LOTE 3 — Checklists", [
            create_doc04,   # Checklist de Conformidade com 3 Políticas
            create_doc07,   # Checklist de Artefatos por Fase do Ciclo de Vida
            create_doc10,   # Checklist de Verificação de Fontes e PI
            create_doc11,   # Checklist de Avaliação para Contratação de IA
        ]),
        ("LOTE 4 — Termos e Templates de Relatório", [
            create_doc08,   # Termo de Ciência e Uso Responsável de IA (.docx)
            create_doc09,   # Template de Documentação de Uso Contínuo de IA Generativa
            create_doc13,   # Template de Parecer do CETIA (.docx)
            create_doc14,   # Template de Relatório de Supervisão Periódica de IA
        ]),
    ]

    total = 0
    errors = []

    for lote_nome, funcs in docs:
        print(f"\n--- {lote_nome} ---")
        for func in funcs:
            try:
                func()
                total += 1
            except Exception as e:
                errors.append((func.__name__, str(e)))
                print(f"  ERRO em {func.__name__}: {e}")
                import traceback
                traceback.print_exc()

    elapsed = time.time() - start

    print()
    print("=" * 70)
    print(f"RESULTADO: {total}/14 documentos gerados com sucesso")
    if errors:
        print(f"ERROS: {len(errors)}")
        for name, err in errors:
            print(f"  - {name}: {err}")
    print(f"Tempo: {elapsed:.1f}s")
    print(f"Diretório: {os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs_operacionais'))}")
    print("=" * 70)


if __name__ == "__main__":
    main()
