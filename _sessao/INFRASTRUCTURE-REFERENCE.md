# Referência de infraestrutura — checklist-conformidade

<!-- endereços, IDs, variáveis e receitas; sem segredos (chaves só no .env local); valores internos da rede da Câmara em INTERNO.md, que não vai para o GitHub público -->

## Endereços e repositórios

| Item | Valor |
|---|---|
| App publicado | https://checklist-conformidade.streamlit.app/ (Streamlit Community Cloud; privado, login de viewer) |
| Remoto `origin` | GitLab interno da Câmara, URL em `INTERNO.md` ( o `master` rastreia este) |
| Remoto `github` | https://github.com/rodilpinto/checklist-conformidade.git (**o Streamlit Cloud publica a partir daqui**) |
| LLM local | endereço em `INTERNO.md`, modelo `google/gemma-4` (llama.cpp; `n_ctx` 20480; velocidade medida em `LICOES.md`). Só é acessível da rede da Câmara |
| Tokenizer do LLM local | `POST <servidor>/tokenize` (raiz, fora do `/v1`; endereço em `INTERNO.md`) com `{"content": "..."}` |
| Gemini | https://generativelanguage.googleapis.com (SDK `google-genai`); compatível com OpenAI: `/v1beta/openai/` |
| Texto oficial da Portaria 227/2025 | URL na primeira linha de `tests/fixtures/portaria_227_2025.txt` |
| Manual de marca da Câmara | `branding/fonte/` (origem: www2.camara.leg.br/comunicacao/assessoria-de-imprensa/uso-da-marca) |

## Variáveis de ambiente (`.env` local; *secrets* no Streamlit Cloud)

| Variável | Uso |
|---|---|
| `GEMINI_API_KEY` | chave `AQ.` da conta Google da unidade (nível gratuito em 23/09/2026) |
| `GEMINI_MODEL` | opcional; padrão `gemini-3.6-flash` |
| `LOCAL_LLM_URL`, `LOCAL_LLM_MODEL` | LLM local |
| `LOCAL_LLM_DISABLE_THINKING` | `1` desliga o raciocínio do Gemma |
| `EXTRACTOR_TRUSTED_DOMAINS` | opcional; padrão `camara.leg.br` |

## Receitas

- **Rodar o app local:** `py -m pip install -r requirements.txt`, depois `cp .env.example .env` e preencher, depois `py -m streamlit run app.py --server.headless true --server.port 8501`. Para reiniciar, ver `LICOES.md`.
- **Testar o LLM local:** `curl -s $LOCAL_LLM_URL/models` (URL no `.env`)
- **Testar a chave Gemini sem exibi-la:** `py -c "from dotenv import load_dotenv; load_dotenv('.env'); import os; from google import genai; print(genai.Client(api_key=os.environ['GEMINI_API_KEY']).models.generate_content(model='gemini-3.6-flash', contents='responda: ok').text)"`
- **Avaliação de modelos:** ver `tests/AVALIACAO_MODELOS.md`, seção 9.
- **Push para o GitLab da Câmara:** `GCM_INTERACTIVE=always git push origin master`, da sessão principal, com o Rodrigo autorizando no navegador.
- **Publicar no Streamlit Cloud:** atualizar os *secrets* e depois `bash scripts/publicar_github.sh`. **Nunca** `git push github master` direto: o GitHub é público, e o script publica um snapshot sem `_sessao/INTERNO.md` e sem o histórico interno, abortando se achar dado de infraestrutura.
