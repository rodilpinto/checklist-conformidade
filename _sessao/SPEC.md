# SPEC — checklist-conformidade

<!-- last_updated: 2026-10-01 · escopo atual; histórico de decisões em DECISOES.md -->

App Streamlit que transforma um normativo (PDF, DOCX, texto ou URL) em checklist de conformidade (Excel). Para cada dispositivo (artigo, parágrafo, inciso, alínea), gera: texto literal, requisito, risco, **responsável**, mitigação, evidência e nota de risco MCGR (Impacto × Probabilidade).

**O essencial** (Rodrigo, 23/09/2026): extrair os dispositivos com fidelidade e atribuir os responsáveis. A nota de risco é referência e será validada por um humano.

## Escopo atual

1. **MVP no ar** (feito, 25/09): Streamlit Cloud com `gemini-3.5-flash-lite`. Desde 30/09, dois ambientes (D-C22): `main` = produção, ainda com o código do MVP; `homologacao` = com o `nuati-framework`.
2. **LLM com fallback entre provedores** (feito na `homologacao`, 30/09): pasta `llm_cadeia/` do framework (local, Gemini, Groq, Cerebras, OpenRouter, chave do usuário). Na produção, ainda o provider do MVP (Gemini ou local). Depois: divisão em lotes e erros reais (patch pausado).
3. **Identidade visual** (feito, aguarda revisão): `branding/`, aplicado neste app.
4. **Avaliação de modelos** (feita a rodada exploratória, pausada): `tests/eval_modelos.py` e `tests/AVALIACAO_MODELOS.md`.
5. **Planilha de saída no padrão v1.08, já como v1.09** (próximo trabalho, Rodrigo, 01/10): colunas e abas novas da v1.08, sem linhas de separação de capítulo, e atores separados (hoje multivalorados). Itens em `TODO.md`.

## Fora do escopo por enquanto

- Próximas rodadas de teste de modelo (P2).
- Aplicar `branding/` nos outros apps (P3).
