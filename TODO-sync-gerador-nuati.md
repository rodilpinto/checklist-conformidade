# TODO: Atualizar o app de deploy com base em `gerador-checklists/`

> Criado em 2026-07-14, quando `gerador-checklists/` foi trazido de `projetos-nuati`
> para este repositório.

## Situação

Este repo agora tem **duas** implementações do gerador de checklist:

1. **App de deploy** (raiz: `app.py`, `lib/`) - interface Streamlit + LLM (Gemini).
   Gera checklist de qualquer normativo. **Está desatualizado.**
2. **`gerador-checklists/`** - scripts one-shot vindos de `projetos-nuati`, que
   produziram os entregáveis validados da auditoria (Portaria 227/2025 v1.06-1.08,
   DOC-01..14). **É a versão mais completa e atual da metodologia.**

## Missão

Atualizar o **app de deploy** (1) para refletir a metodologia mais completa que
está em **`gerador-checklists/`** (2).

- [ ] Comparar `lib/excel_builder.py` e `lib/prompt_templates.py` com
      `gerador-checklists/scripts/create_v108.py` e
      `gerador-checklists/data/scoring_risco_v108.json`.
- [ ] Portar para o app a metodologia de scoring atual (Criticidade =
      Impacto(1-5) x Probabilidade(1-5); faixas Baixo/Moderado/Alto/Muito alto)
      e o modelo MCGR da Câmara.
- [ ] Alinhar o schema de saída (capitulo, artigo, texto_literal, requisito,
      risco, nivel, mitigacao, responsavel, evidencia) ao dos entregáveis validados.
- [ ] Preservar regras: texto literal nunca parafraseado; terminologia oficial
      (Encarregado de Proteção de Dados Pessoais, forma oficial da Portaria
      227/2025, decidida em 2026-09-22; CETIA).
- [ ] Rodar o app atualizado e comparar a saída com os `.xlsx` de referência em
      `gerador-checklists/checklists/`.

## Observação de proveniência

Os `.xlsx` em `gerador-checklists/checklists/` e `gerador-checklists/docs_operacionais/`
são os **entregáveis validados** da auditoria. Servem de referência ("golden output")
para validar o app; não devem ser regenerados sem revisão humana.
