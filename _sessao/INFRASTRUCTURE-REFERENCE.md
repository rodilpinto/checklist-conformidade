# Referência de infraestrutura — checklist-conformidade

<!-- endereços, IDs, variáveis e receitas; sem segredos (chaves só no .env local); valores internos da rede da Câmara em INTERNO.md, que não vai para o GitHub público -->

## Endereços e repositórios

| Item | Valor |
|---|---|
| App de produção (`main`) | https://checklist-conformidade.streamlit.app/ (Streamlit Community Cloud; **público** desde 25/09). Recriado em 30/09 na branch `main` do GitHub (D-C22); ainda **sem o framework** (código do antigo `master`) |
| App de homologação (`homologacao`) | https://checklist-conformidade-homologacao.streamlit.app/ (criado em 30/09). Segue `github/homologacao`, com o framework. O antigo `-v2` foi apagado em 01/10 |
| Remoto `origin` | servidor git interno da Câmara (Gitea, não GitLab; URL em `INTERNO.md`); origem do histórico completo; branch padrão `main` (trocada pelo Rodrigo em 01/10) |
| Remoto `github` | https://github.com/rodilpinto/checklist-conformidade.git (**o Streamlit Cloud publica a partir daqui**) |
| LLM local | endereço em `INTERNO.md`, modelo `google/gemma-4` (llama.cpp; `n_ctx` 20480; velocidade medida em `LICOES.md`). Só é acessível da rede da Câmara |
| Tokenizer do LLM local | `POST <servidor>/tokenize` (raiz, fora do `/v1`; endereço em `INTERNO.md`) com `{"content": "..."}` |
| Gemini | https://generativelanguage.googleapis.com (SDK `google-genai`); compatível com OpenAI: `/v1beta/openai/` |
| Texto oficial da Portaria 227/2025 | URL na primeira linha de `tests/fixtures/portaria_227_2025.txt` |
| Manual de marca da Câmara | `branding/fonte/` (origem: www2.camara.leg.br/comunicacao/assessoria-de-imprensa/uso-da-marca) |

## Variáveis de ambiente (`.env` local; *secrets* no Streamlit Cloud)

A tabela abaixo é a do código da `main` (produção, sem framework). Na `homologacao`, os nomes são os da tabela "Segredos" de `llm_cadeia/README.md`; o bloco padrão comum e a exceção do app principal estão em `DECISOES.md` (28/09).

| Variável | Uso |
|---|---|
| `GEMINI_API_KEY` | chave `AQ.` da conta Google da unidade (nível gratuito em 23/09/2026) |
| `GEMINI_MODEL` | opcional; padrão do código `gemini-3.6-flash`; **no Streamlit Cloud: `gemini-3.5-flash-lite`** (25/09) |
| `LOCAL_LLM_URL`, `LOCAL_LLM_MODEL` | LLM local |
| `LOCAL_LLM_DISABLE_THINKING` | `1` desliga o raciocínio do Gemma |
| `EXTRACTOR_TRUSTED_DOMAINS` | opcional; padrão `camara.leg.br` |

## Receitas

- **Rodar o app local:** `py -m pip install -r requirements.txt`, depois `cp .env.example .env` e preencher, depois `py -m streamlit run app.py --server.headless true --server.port 8501`. Para reiniciar, ver `LICOES.md`.
- **Testar o LLM local:** `curl -s $LOCAL_LLM_URL/models` (URL no `.env`)
- **Testar a chave Gemini sem exibi-la:** `py -c "from dotenv import load_dotenv; load_dotenv('.env'); import os; from google import genai; print(genai.Client(api_key=os.environ['GEMINI_API_KEY']).models.generate_content(model='gemini-3.6-flash', contents='responda: ok').text)"`
- **Rodar os testes:** `py -m pytest -q` da raiz (inclui os testes das pastas do framework).
- **Avaliação de modelos:** ver `tests/AVALIACAO_MODELOS.md`, seção 9.
- **Push para o servidor git interno (Gitea):** `git push origin <branch>` costuma funcionar direto (credencial em cache); se der "Authentication failed", `GCM_INTERACTIVE=always git push origin <branch>` da sessão principal, com o Rodrigo autorizando no navegador. Repositório novo precisa ser criado antes pela tela (o servidor não cria por push).
- **Publicar uma branch no GitHub** (desde 30/09, recurso `publicar_snapshot` do framework): `bash publicar_snapshot/publicar_snapshot.sh --ramo <branch>` (`main` alimenta a produção, `homologacao` o app de homologação; sem `--ramo`, publica a `main`). Use `--simular` antes, para ver o que muda. Configuração do app (exclusões e padrões da trava) em `publicar_snapshot.conf`, que nunca vai para o snapshot.
- **Publicar no Streamlit Cloud:** atualizar os *secrets* e depois `bash publicar_snapshot/publicar_snapshot.sh --ramo <branch>`. **Nunca** `git push github` direto (em nenhuma branch): o GitHub é público, e o script publica um snapshot sem `_sessao/INTERNO.md` e sem o histórico interno, abortando se achar dado de infraestrutura.

## Ambientes (D-C22, desde 30/09/2026)

| Branch | Papel | App |
|---|---|---|
| `main` | estável (produção); padrão no GitHub | checklist-conformidade.streamlit.app |
| `homologacao` | trabalho do dia a dia | checklist-conformidade-homologacao.streamlit.app |

Receita do dia a dia (trabalhar, testar na homologação, promover com tag, voltar atrás) e regra de sincronia das pastas do framework: README do `nuati-framework`, §2 e §3. Neste app, todo push no interno é seguido do snapshot da branch que mudou (`bash publicar_snapshot/publicar_snapshot.sh --simular --ramo <branch>` e depois sem `--simular`); para publicar uma branch que não é a aberta, use um worktree (`LICOES.md`, 30/09). Tags de retorno: `pre-framework-2026-09-30-master`, `pre-framework-2026-09-30-feat-llm-cadeia`, `pre-llm-cadeia`.

## Fluxo de versões: estável no ar, trabalho em branches (decidido em 28/09/2026)

> ⚠ **Superado em 29/09 pela D-C22** (`main` estável + `homologacao` playground, app `<app>-homologacao`; `buscador-normativos/_DECISOES-PENDENTES.md`). A receita nova vai morar no README do framework (D-C23). O texto abaixo fica só como histórico e insumo.

```
feat/<assunto>  →  homologacao  →  app v2 (teste)  →  master + tag  →  app principal
```

| Branch | Papel | Publica em |
|---|---|---|
| `master` | **só versão estável**, já testada no v2; cada publicação ganha uma tag | app principal |
| `homologacao` | versão candidata, em teste | app v2 |
| `feat/<assunto>` | trabalho em andamento, uma por assunto | só local e GitLab |

**Receita de cada etapa:**

1. **Começar um trabalho:** `git switch master && git switch -c feat/<assunto>`. Faça commits e envie ao GitLab (`git push origin feat/<assunto>`).
2. **Testar no v2:**
   1. `git switch homologacao && git merge feat/<assunto>`.
   2. Confira os *secrets* do v2 contra as variáveis que o código lê (`grep -rn "getenv\|st.secrets\|_segredo(" --include=*.py .`).
   3. Publique com `bash scripts/publicar_github.sh --simular --ramo homologacao` e depois sem o `--simular`.
   4. Teste no v2 com um texto curto e com a Portaria 227 inteira.
3. **Promover para o app principal** (só com o ok do Rodrigo):
   1. `git switch master && git merge homologacao`.
   2. `git tag -a vX.Y -m "<o que mudou>"`.
   3. `git push origin master vX.Y`.
   4. Ajuste os *secrets* do principal para o que o código novo lê.
   5. `bash scripts/publicar_github.sh --simular` e depois sem o `--simular`.
   6. Teste o principal com os mesmos dois casos.
4. **Voltar atrás, se o principal quebrar:** `git switch -c conserto <tag-anterior>` e publique essa árvore no `master` do GitHub (📝 o script ainda não tem essa opção; por enquanto, peça ao Claude). Devolva também os *secrets* anteriores.

**Regras:**
- Nada vai ao `master` sem passar pelo v2.
- Trocar *secrets* também é deploy, e os dois apps dividem a cota do Gemini: ver `LICOES.md` (28/09 e 25/09).
