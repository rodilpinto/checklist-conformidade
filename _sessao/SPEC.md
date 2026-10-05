# SPEC — checklist-conformidade

<!-- last_updated: 2026-10-01 · escopo atual; histórico de decisões em DECISOES.md -->

App Streamlit que transforma um normativo (PDF, DOCX, texto ou URL) em checklist de conformidade (Excel). Para cada dispositivo (artigo, parágrafo, inciso, alínea), gera: texto literal, requisito, risco, **responsável**, mitigação, evidência e nota de risco MCGR (Impacto × Probabilidade).

**O essencial** (Rodrigo, 23/09/2026): extrair os dispositivos com fidelidade e atribuir os responsáveis. A nota de risco é referência e será validada por um humano.

## Escopo atual

1. **MVP no ar** (feito, 25/09): Streamlit Cloud com `gemini-3.5-flash-lite`. Desde 30/09, dois ambientes (D-C22): `main` = produção, ainda com o código do MVP; `homologacao` = com o `nuati-framework`. Desde 01/10, a `main` roda também no **servidor do Nuati** (rede interna, LLM local + Gemini; `servidor/`).
2. **LLM com fallback entre provedores** (feito na `homologacao`, 30/09): pasta `llm_cadeia/` do framework (local, Gemini, Groq, Cerebras, OpenRouter, chave do usuário). Na produção, ainda o provider do MVP (Gemini ou local). Depois: divisão em lotes e erros reais (patch pausado).
3. **Identidade visual** (feito, aguarda revisão): `branding/`, aplicado neste app.
4. **Avaliação de modelos** (feita a rodada exploratória, pausada): `tests/eval_modelos.py` e `tests/AVALIACAO_MODELOS.md`.
5. **Planilha de saída no padrão v1.08, já como v1.09** (código na `homologacao`, 01/10; decisões em `DECISOES.md`): colunas da v1.08 (menos "Nível (v1.06)"), ordem por criticidade, sem linhas de capítulo, abas Ações por Ator (uma linha por item × ator), Resumo por Capítulo e Legenda. Fora: aba "Curso" e coluna "Fase". Itens em `TODO.md`.

## Fora do escopo por enquanto

- Próximas rodadas de teste de modelo (P2).
- Aplicar `branding/` nos outros apps (P3).
