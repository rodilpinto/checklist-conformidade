# log — checklist-conformidade

<!-- linha do tempo, mais recente no topo; só acrescentar -->

## 2026-10-01 | passe por app: passos 8 a 10 (limpeza, registro, journal)

- O Rodrigo validou o dropdown do tempo economizado e deu o OK para o passo 8.
- `main` virou a branch padrão do GitHub (`gh repo edit`). Apagados, com confirmação dele: o app `-v2` (pelo Rodrigo), `master` e `feat/llm-cadeia` no GitHub (pela API), `feat/llm-cadeia` no interno, `master` e `feat/llm-cadeia` locais. Conferido antes: `master` = `main` e `feat/llm-cadeia` contida na `homologacao`; as tags `pre-framework-*` estão no interno.
- O Rodrigo trocou a branch padrão do Gitea interno para `main`; em seguida o `master` interno foi apagado (era igual à `main`, `eab1039`).
- Registro de cópias no README §4 do framework (só as linhas do checklist), commit `975970b` na `homologacao` do `nuati-framework`.

## 2026-09-30 | passe por app: passos 6 e 7 (apps no ar e conferência)

- Passo 6 (Rodrigo): produção recriada na mesma URL na branch `main`, com os mesmos Secrets; `checklist-conformidade-homologacao` criado na `homologacao`.
- Homologação abriu com `StreamlitAPIException` ("←" não é emoji) no aviso de "nenhum modelo configurado": bug do app, corrigido em `1598bf1` (snapshot `8133664`). A causa de fundo era o app sem chave visível; com **Reboot**, funcionou (o `llm_cadeia` lê os Secrets no início do processo).
- Log da nuvem: `local` falhou com `ConnectTimeoutError` (IP interno inalcançável fora da rede) e ficou 300 s em espera; a cadeia seguiu para o Gemini. Comportamento esperado (LESSONS do framework).
- Passo 7, conferido pelo Claude no navegador (Playwright), 01/10 ~01:12-01:19 UTC:
  - homologação, `branding`: título da aba "… | Câmara dos Deputados", cabeçalho com o logo, rodapé com a assinatura das unidades e o logo;
  - `llm_cadeia`: barra lateral com a cadeia em ordem (local, gemini, gemini-2, groq-2, cerebras-2, openrouter-2) e o campo de chave própria; cada geração mostrou "Gerado por gemini (gemini-3.5-flash-lite)";
  - `extracao_texto`: PDF e DOCX de teste (Arts. 10 e 11) viraram 2 itens com esses artigos (conferido no Excel baixado); a URL oficial da Portaria 227 gerou 83 itens em cerca de 1 min 15 s;
  - `tempo_economizado`: linha e dropdown aparecem; 2 itens = 18 min, 83 itens = 12h27min (9,0 × itens). A clareza da explicação para quem não conhece a conta fica para o julgamento do Rodrigo;
  - `publicar_snapshot`: snapshots publicados sem exceção na trava;
  - produção: tela antiga do `master` (seletor Gemini/local, chave configurada), geração curta deu "2 itens gerados, tempo manual estimado: 18 min".

## 2026-09-30 | passe por app: framework na homologação (passos 0 a 5)

- Passo 0 (confirmado pelo Rodrigo): `master` (app principal) → `main`; `feat/llm-cadeia` (app `-v2`) → `homologacao`; produção sem framework nesta rodada. Entre o snapshot no ar (`69f8c53`) e o `master` interno (`eab1039`), só documentação e `.gitattributes` mudam.
- Passo 1: tags anotadas `pre-framework-2026-09-30-master` (`eab1039`) e `pre-framework-2026-09-30-feat-llm-cadeia` (`0401040`), enviadas ao interno.
- Passo 2, linha de base: 19 testes passam (todos do `llm_cadeia` 1.0.0); fumaça com `AppTest` sem exceção.
- Passo 3, `homologacao` (de `feat/llm-cadeia`), framework @ `29880aa`, cópia por `git archive` e hashes conferidos contra a origem:
  - `llm_cadeia` 1.1.0 (`2075aa1`): a cópia 1.0.0 tinha o código idêntico ao buscador @ `3edba4d`; só o README tinha uma linha de procedência posta na adoção (`2357a2e`), sem edição de código. `tests/eval_modelos.py` adaptado. 31 testes.
  - `branding` 1.0.0 (`f84d7e9`), `extracao_texto` 1.0.0 (`aff5294`, sai `lib/extractor.py`, mesmo hash), `tempo_economizado` 1.0.0 (`9c19a60`, mesmos minutos; número igual de 1 a 118 itens, ex.: 92 itens = 13h48min), `publicar_snapshot` 1.0.0 (`3dfd59e`, sai `scripts/publicar_github.sh`; trava sem exceção).
  - Testes depois: 113 passam, 1 `xfail` (defeito conhecido do `extracao_texto`); fumaça sem exceção.
  - `python -m llm_cadeia` (chaves carregadas no processo): local, gemini, gemini-2, groq-2, cerebras-2 e openrouter-2 respondem em ao menos um modelo; 404 nos `gemini-2.5-*` da chave sem sufixo, 500 no `gemma-4-31b-it` do Gemini, 429 nos `:free` nomeados do OpenRouter.
  - Geração local com a Portaria 227 inteira (cadeia completa, `lib.llm.generate_checklist`): com raciocínio, o `local` estourou os 300 s e o `gemini-3.5-flash-lite` respondeu, 362 s no total, 79 itens válidos. Sem raciocínio (`LLM_DISABLE_THINKING=1`): o `local` também estourou os 300 s, e o `gemini-3.5-flash-lite` respondeu, 351 s no total, 84 itens válidos. 📝 Leitura: com o normativo inteiro numa chamada, o Gemma não termina em 300 s nem sem raciocínio (o trecho de 5.000 caracteres levou 54 s em 28/09); a saída estrutural continua sendo a divisão em lotes (patch pausado). O log não mostra se o campo `enable_thinking` foi aceito nessa chamada (o framework conferiu que o servidor aceita em 29/09).
- Passo 4: `main` = `master` (`eab1039`) no interno; snapshots no GitHub `main` = `3709a25` (primeiro snapshot, sem pai) e `homologacao` = `2233c9a`, sem `INTERNO.md` nem `.conf`. Defeito do `publicar_snapshot` ao publicar a `main` a partir da `homologacao` aberta, contornado com worktree (`LICOES.md`).
- Passo 5: *Secrets* × código levantados; blocos entregues ao Rodrigo (`BLOCKED-ON-RODRIGO.md`).

## 2026-09-29 | checkpoint da pausa e entregas para o framework

- Entregue à sessão do framework: `solucoes/framework/LEVANTAMENTO-FRAMEWORK.md` (repositório `Nuati-SECIN/framework` @ `4c751ba`), com os candidatos por tema nos 8 apps, os defeitos do `llm_cadeia`, as lições e a situação daquele repositório.
- Revisão adversária (5 revisores) do plano de scripts do framework: achou bugs de perda de dados (D1 a D3 nas emendas de `solucoes/framework/docs/plans/2026-09-28-esqueleto.md`) e excesso de complexidade; o Rodrigo abandonou os scripts em favor de copiar e colar com log de versões. Plano e spec marcados como superados.
- Checkpoint: arquivo de estado reescrito para a pausa; TODO, DECISOES, BLOCKED-ON, LICOES, INFRASTRUCTURE-REFERENCE e onboard atualizados; snapshot `checklist_state_2026-09-29.md` na memória.

## 2026-09-29 | pausa para o framework (D-C23), branch feat/llm-cadeia @ a6df684

- Pedido do Rodrigo, a partir das decisões D-C22, D-C23 e D-C24 (`buscador-normativos/_DECISOES-PENDENTES.md` @ `ab8011b`): o framework central passa a ser o repositório privado `rodilpinto/nuati-framework`. Cada app vai receber um passe único, que adota o framework e migra para `main` (estável) e `homologacao` (playground).
- Estado da pausa: trabalho em `feat/llm-cadeia` @ `a6df684` (mais o commit deste registro). `master` intocado (`eab1039`, tag `pre-llm-cadeia`); `github/master` = `090aa67` (app principal no ar); `github/feat/llm-cadeia` = `da8ccd4` (app v2).
- A partir de agora, a pasta `llm_cadeia/` fica **congelada** (D-C24): cópia 1.0.0 (buscador @ `3edba4d`). Os defeitos achados aqui viram pedido à sessão do framework; conferido em 29/09 que **nenhum** dos 5 pedidos do `TODO.md` (P0) foi corrigido na 1.0.1 do buscador.
- ⚠ Superado pela D-C22: o fluxo `master` + `homologacao` + app "-v2" registrado em 28/09. O novo é `main` + `homologacao`, com app `<app>-homologacao`, a ser feito no passe por app.
- ⚠ Superado pela D-C23 e pela decisão do Rodrigo de 29/09 ("abandonar a ideia de scripts; começar com copia e cola e log de versões"): o repositório `Nuati-SECIN/framework` no servidor interno, com spec e plano de scripts, criado nesta sessão em 28/09. Fica como histórico e insumo para a sessão nova.

## 2026-09-28 (noite) | incidente no app principal: secrets padronizados

- Sintoma relatado pelo Rodrigo: o app principal deu primeiro só 1 artigo e, na segunda vez, "Erro na comunicacao com o modelo Gemini" (mensagem genérica do código antigo). O log tinha 2 tracebacks `StreamlitAPIException: The value "←" is not a valid emoji` (em `app.py:547`), que só aparecem quando o app acha que não há `GEMINI_API_KEY`.
- ✅ Não foi o código: o `github/master` continuava no `090aa67` (25/09), e o app tinha reiniciado às 20:03 UTC, antes desta sessão mexer em qualquer coisa.
- Causa provável, admitida pelo Rodrigo ("acho que alterei em todos os secrets"): ao padronizar os *secrets* de todos os apps para os nomes do `llm_cadeia`, o app principal perdeu o `GEMINI_MODEL = "gemini-3.5-flash-lite"` e voltou ao padrão do código antigo, `gemini-3.6-flash`, que dá 503 com textos grandes. O `GEMINI_API_KEY` passou a ser a chave sem sufixo, que deu 503 hoje e divide a cota com o buscador.
- Correção feita pelo Rodrigo nos *secrets* do app principal: acrescentou `GEMINI_MODEL = "gemini-3.5-flash-lite"` (a linha também vai para o bloco padrão de todos os apps, e o `llm_cadeia` a ignora); pôs em `GEMINI_API_KEY` o valor da chave `_2` (exceção temporária, só no app principal e só até o merge); fez Reboot.
- ✅ Teste depois da correção, no app principal, com a Portaria 227 inteira pelo link: **92 itens**, cerca de 2,5 min. Screenshot em `.playwright-mcp/principal-portaria227-92itens-2026-09-28.png`.

## 2026-09-28 (noite) | app v2 no ar e testes na nuvem

- O Rodrigo criou o segundo app, https://checklist-conformidade-v2.streamlit.app/ (branch `feat/llm-cadeia`). A branch não aparecia na lista do "Create app", mas foi aceita. Os *secrets* incluem `LLM_BASE_URL`, e por isso a lista mostra `local` em primeiro lugar, embora a nuvem não o alcance.
- ✅ Nuvem, texto curto (Arts. 8º e 9º): 2 itens, "Gerado por gemini (gemini-3.5-flash-lite)". Screenshot em `.playwright-mcp/llm-cadeia-v2-nuvem-2026-09-28.png`.
- ❌ Nuvem, Portaria 227 inteira pelo link: a 1ª tentativa deu "Não foi possível interpretar a resposta do modelo como JSON" (menos de 2,5 min); a 2ª ficou parada em "Etapa 2" por mais de 8 min, e parei de esperar.
- ✅ Local, mesmo caminho (URL → `generate_checklist`, só o Gemini com a chave `_2`): 24.268 caracteres, 118 itens válidos em 66 s. Local com o arquivo de teste, `max_tokens=32768`: 92 e 98 itens em 53 s (80 mil caracteres de resposta). **A falha não se reproduziu localmente.**
- 📝 Hipóteses, não confirmadas: (a) o teto de `_MAX_TOKENS=32768` que eu escolhi fica perto do tamanho da resposta (de 92 a 118 itens, cerca de 80 a 95 mil caracteres), e uma resposta maior seria cortada no meio do JSON; o MVP não definia teto. (b) O transporte Gemini do `llm_cadeia` **não tem tempo limite** (só o `local` tem), o que explica a tela parada. Para confirmar, faltam os logs do app na nuvem ("Manage app" → logs).
- **Logs da nuvem** (colados pelo Rodrigo) e desfecho:
  - 1ª tentativa com a Portaria: não há falha registrada, ou seja, o `gemini-3.5-flash-lite` (chave sem sufixo) **respondeu**, e o JSON veio inválido. A causa (resposta cortada ou malformada) não aparece no log.
  - 2ª tentativa: local por tempo de conexão (5 s); na chave sem sufixo, 503 no flash-lite, no flash, no 3-flash-preview e no gemma-4-31b-it e 404 nos 2.5; depois, o `gemini-2 (gemini-3.5-flash-lite)` atendeu. **Terminou por volta das 22:20: 47 itens**, cerca de 7,5 min depois do clique. A tela "travada" era só lentidão.
  - 📝 47 itens contra 92 a 118 nas rodadas locais: a cobertura varia muito entre chamadas. Não validei os itens.
- Decisão do Rodrigo: manter os *secrets* **iguais em todos os apps**, inclusive `LLM_BASE_URL` na nuvem. Custo medido: 5 s de tempo de conexão por tentativa, com o `local` fora por 5 min por processo.
- Push de `feat/llm-cadeia` e da tag `pre-llm-cadeia` ao GitLab funcionou direto, sem pedir login (a credencial já estava em cache, depois que outra sessão acessou o GitLab).
- Comportamento anterior à branch, visto no teste: o texto colado tem prioridade sobre o link. Com as duas abas preenchidas, o link é ignorado sem aviso.

## 2026-09-28 | llm_cadeia adotado na branch feat/llm-cadeia (versão no ar congelada)

- Versão no ar congelada para a reunião de 29/09: tag `pre-llm-cadeia` no `eab1039`, trabalho na branch `feat/llm-cadeia`, nenhum push em `master` nem no `github`.
- `llm_cadeia/` copiado do buscador-normativos @ `3edba4d` (v1.0.0) com `git archive`. `diff -r` contra a origem: só a linha "Copiado de..." no README.
- `lib/llm.py`: `_call_gemini`, `_call_local_llm` e `_handle_api_error` saem. O `generate_checklist(text, extra_prompt)` chama `gerar(..., sistema=build_prompt(), json=True, temperatura=0.1, max_tokens=32768)` e devolve `(itens, origem)`. Sem resposta, levanta `LLMError` com a lista de tentativas. O `_parse_json_response` e o `validate_items` não mudaram.
- `app.py`: `painel_llm()` na barra lateral, no lugar do botão Gemini/local. O botão "Gerar" é liberado quando `llm_cadeia.disponivel()`. "Gerado por ..." no resultado. `st.rerun()` depois da geração, para a barra lateral mostrar "Última resposta". `.env.example` com os nomes novos.
- Verificação ao vivo, nesta máquina (rede da Câmara):
  - `pytest llm_cadeia/test_llm_cadeia.py`: 19 passed.
  - `python -m llm_cadeia`: todos os provedores externos passam pela rede (detalhes em `LICOES.md`).
  - Só o local, chamada mínima com `sistema=` + `json=True`: 7,7 s, e `json.loads` funciona. Com o prompt real e um trecho de 5.000 caracteres: estouro de tempo em 120 s (a medição direta deu 154 s com raciocínio e 54 s sem).
  - App local na porta 8502, colando os Arts. 8º e 9º: "2 itens", "Gerado por local (google/gemma-4)" e "Última resposta: local (google/gemma-4)" na barra lateral. Screenshot em `.playwright-mcp/llm-cadeia-local-2026-09-28.png`. A resposta demorou cerca de 5 min, provavelmente por fila no servidor com pedidos abandonados dos testes anteriores (📝 hipótese, não confirmada).
- Testes que o projeto já tinha: não havia suíte pytest. O `tests/eval_modelos.py` é um script de avaliação e quebra com a assinatura nova (pendência no `TODO.md`).
- Auditoria da documentação removida e destino de cada item:
  - docstring antiga (providers e parâmetros) → novo docstring do módulo mais a tabela de segredos do `llm_cadeia/README.md`;
  - `_MODEL_NAME` → `DECISOES.md` (28/09);
  - `_LOCAL_TIMEOUT_SECONDS=300` e seu comentário → pedido 1 à origem;
  - `LOCAL_LLM_DISABLE_THINKING` → pedido 2;
  - comentário sobre modelos "lite" recusarem `thinking_budget` → já está em `LICOES.md` de 25/09 (o módulo não envia `thinking_config`);
  - validação do formato da chave (`AIza`/`AQ.`) → removida; o módulo trata chave inválida como 401/403, e o formato está em `DECISOES.md` de 22/09;
  - `RateLimitError`/`TokenLimitError` e as mensagens amigáveis em português → substituídas pela lista de tentativas (cru, em inglês). 📝 Candidato a melhoria da tela, junto com o patch pausado de mensagens de erro.
- Pedidos para a origem (tempo limite, raciocínio, dados internos, forçar provedor) no `TODO.md`. De início, o deploy da branch ia esperar a v1.0.1 limpa. Depois, o Rodrigo decidiu publicar assim mesmo: o `publicar_github.sh` ganhou `--ramo` e uma exceção na trava só para `llm_cadeia/`, e a branch foi publicada no GitHub.

## 2026-09-25 | MVP no ar com gemini-3.5-flash-lite

- O erro no app publicado era a mensagem genérica. Com o app tornado público, testei: um texto curto funcionava; com texto grande, o `gemini-3.6-flash` gratuito dava 503.
- Levantamento do buscador e do scopediagram: nenhum dos dois tem sequência de chaves. O buscador usa `gemini-3.5-flash-lite` e requisições pequenas.
- O Rodrigo pausou a divisão em lotes e as mensagens de erro reais, para evitar regressão (patch versionado). Commit `69f8c53`: modelos "lite" sem `thinking_budget`. Publicado; *secrets* com o flash-lite e a chave do Rodrigo; **funcionou**.
- Próximo: módulo comum de provedores e chaves, feito na sessão do buscador. Checkpoint.

## 2026-09-23 | publicação no GitHub público

- Descoberto que o GitHub `rodilpinto/checklist-conformidade` é público. IP do LLM, conta Google, GitLab interno e nome de colega foram movidos para `_sessao/INTERNO.md`, com marcadores no restante.
- `scripts/publicar_github.sh` publica um snapshot sem `INTERNO.md` e sem `gerador-checklists/` (material de auditoria; decisão do Rodrigo), com trava que aborta se achar dado interno.
- Primeiro snapshot publicado; o Streamlit Cloud republicou. Depois, o Rodrigo liberou o `gerador-checklists/`, e ele foi incluído num segundo snapshot. O app só funciona depois que o Rodrigo atualizar os *secrets*.

## 2026-09-23 | testes de modelo (rodada 2), pesquisa do Gemini, commit e push, checkpoint

- Rodada 2 de testes: lotes de artigos (800, 1.500 e 3.000 tokens) × Gemma com e sem raciocínio, mais subagentes Opus, Sonnet e Haiku nos mesmos lotes, sem acesso à referência. Novas métricas: responsáveis (condicional e efetiva) e granularidade.
- O Rodrigo definiu o essencial (dispositivos e responsáveis; a nota de risco é só referência) e confirmou que os scores do v1.08 não foram revisados.
- O Rodrigo discordou da leitura sobre os lotes de 1.500; a métrica condicional estava enviesada. Corrigido e documentado em `tests/AVALIACAO_MODELOS.md`.
- Pesquisa do Gemini: faturamento, preço e uso dos dados no nível gratuito (`DECISOES.md`).
- Commit `dcc3ca3` (85 arquivos) enviado ao `origin`, com o login do Rodrigo no navegador. O `github` continua em `3af230a`.
- Nova prioridade: pôr no ar uma versão funcional. Checkpoint para abrir uma sessão nova.

## 2026-09-22 | deploy investigado, provider LLM local, branding, rodada 1 de testes

- Descoberto o app em checklist-conformidade.streamlit.app (privado; a chave Gemini antiga tinha caído).
- `lib/llm.py`: provider local OpenAI-compatible (Gemma 4 no servidor interno), `gemini-3.6-flash`, chaves `AQ.`. `lib/extractor.py`: allowlist `camara.leg.br` no anti-SSRF.
- `branding/` criado a partir do MIV v4.00 da Câmara e aplicado ao app.
- Terminologia oficial "Encarregado de Proteção de Dados Pessoais" no prompt.
- Rodada 1 de testes (documento inteiro × por capítulo): o Gemma resume o documento inteiro; o Gemini gratuito dá 503 e 429.
- `_sessao/` criado (convenção project-journal).
