# Checklist de Conformidade Normativa

App Streamlit que transforma leis, portarias e decretos em checklists de auditoria,
usando IA para extrair artigos/incisos e classificar riscos segundo a metodologia
MCGR da Câmara dos Deputados.

## Deploy

- **App público (Streamlit Community Cloud):** https://checklist-conformidade.streamlit.app/
  - Requer autenticação de viewer (app privado/restrito).
  - **Limitação importante:** o provider "LLM local" (ver abaixo) só funciona
    quando o app roda dentro da rede interna da Câmara — o Streamlit Cloud público
    não alcança endereços da rede interna da Câmara.

## Configuração (Gemini ou LLM local)

Copie `.env.example` para `.env` e configure **um dos dois** providers:

1. **Google Gemini** (nuvem) — `GEMINI_API_KEY`, obtida em
   [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
2. **LLM local** (rede interna, servidor OpenAI-compatible como LM Studio) —
   `LOCAL_LLM_URL` e `LOCAL_LLM_MODEL`.

A escolha entre os dois é feita na sidebar do app em tempo de execução.

## Rodando localmente

```bash
pip install -r requirements.txt
cp .env.example .env   # preencha as variáveis
streamlit run app.py
```

## Estrutura

- `app.py` — interface Streamlit.
- `lib/` — extração de texto, prompt, integração com LLM, geração de Excel.
- `gerador-checklists/` — scripts one-shot da metodologia mais completa
  (ver `TODO-sync-gerador-nuati.md` para o plano de sincronização com o app).

## Identidade visual e avaliação de modelos

- `branding/`: guia de identidade visual dos apps NUATI, baseado no Manual de Identidade Visual da Câmara.
- `tests/AVALIACAO_MODELOS.md`: método e resultados da comparação de modelos (Gemma 4 local, Claude, Gemini). Script: `tests/eval_modelos.py`.
- `_sessao/`: decisões, lições, pendências e escopo atual.
