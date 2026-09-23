# SPEC — checklist-conformidade

<!-- last_updated: 2026-09-23 · escopo atual; histórico de decisões em DECISOES.md -->

App Streamlit que transforma um normativo (PDF, DOCX, texto ou URL) em checklist de conformidade (Excel). Para cada dispositivo (artigo, parágrafo, inciso, alínea), gera: texto literal, requisito, risco, **responsável**, mitigação, evidência e nota de risco MCGR (Impacto × Probabilidade).

**O essencial** (Rodrigo, 23/09/2026): extrair os dispositivos com fidelidade e atribuir os responsáveis. A nota de risco é referência e será validada por um humano.

## Escopo atual

1. **Versão funcional no ar** (P0, em andamento). O app precisa dividir o normativo em lotes (~800 tokens), mostrar o progresso, tentar de novo em falhas transitórias e exibir erros reais. Depois, publicar conforme a decisão de hospedagem. Plano em `TODO.md`.
2. **Provider de LLM configurável** (feito): Gemini (`gemini-3.6-flash`) ou LLM local OpenAI-compatible (Gemma 4), com opção de desligar o raciocínio.
3. **Identidade visual** (feito, aguarda revisão): `branding/`, aplicado neste app.
4. **Avaliação de modelos** (feita a rodada exploratória, pausada): `tests/eval_modelos.py` e `tests/AVALIACAO_MODELOS.md`.

## Fora do escopo por enquanto

- Incorporar os elementos do v1.08 (P1, logo depois do deploy).
- Próximas rodadas de teste de modelo (P2).
- Aplicar `branding/` nos outros apps (P3).
