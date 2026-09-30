# TODO — checklist-conformidade

<!-- last_audit: 2026-09-29 · itens concretos, mais urgentes no topo · ações que só o Rodrigo pode fazer: BLOCKED-ON-RODRIGO.md (raiz) -->

## ⏸ Em pausa desde 29/09 (D-C23): tudo abaixo espera o passe por app

O próximo trabalho neste app é o **passe por app** (D-C23): adotar o framework `rodilpinto/nuati-framework` e migrar para `main` + `homologacao` (D-C22), num passe só. Os itens do P0 são insumo para esse passe. `llm_cadeia/` está congelada (D-C24): os pedidos abaixo vão para a sessão do framework, e **nenhum** estava corrigido na 1.0.1 (conferido em 29/09; cópia para ela em `solucoes/framework/LEVANTAMENTO-FRAMEWORK.md`, seção A).

## P0: módulo comum de provedores e chaves de LLM (a partir de 25/09/2026)

- [x] (28/09) `llm_cadeia` 1.0.0 (buscador @ `3edba4d`) adotado na branch `feat/llm-cadeia`. Tag `pre-llm-cadeia` marca a versão no ar. Detalhes no `log.md` de 28/09.
- [ ] **Pedidos para a origem (agora a sessão do framework, D-C24), a serem corrigidos lá e recopiados. Não editar a cópia:**
  1. **Tempo limite do LLM local de 120 s é curto** (`nucleo.py`, `timeout=(5, 120)`). Medido em 28/09, trecho de 5.000 caracteres da Portaria 227 com o prompt do app: 154 s com raciocínio (como o módulo envia), 54 s sem. Resultado: o `local` nunca atende um normativo real, e a cadeia passa para o Gemini. O app antigo usava 300 s.
  2. **Não há como desligar o raciocínio do Gemma** (`chat_template_kwargs: {enable_thinking: false}`; no app antigo, `LOCAL_LLM_DISABLE_THINKING=1`). Sem ele, a mesma chamada cai de 154 s para 54 s.
  3. **A pasta tem dados internos** (IP do servidor local e login da conta Google) no `README.md`, no `nucleo.py` (docstring e comentário) e no `test_llm_cadeia.py`. 📝 Continua valendo como higiene na origem, mas **não bloqueia mais**: em 28/09, o Rodrigo decidiu publicar assim mesmo (exceção na trava; ver `DECISOES.md`).
  4. 📝 Não há como forçar um só provedor num teste: `_segredo` lê `st.secrets` antes das variáveis de ambiente, e o `st.secrets` carrega o `~/.streamlit/secrets.toml` global mesmo fora do `streamlit run`. O `LLM_ORDEM` só reordena. Isso afeta o `tests/eval_modelos.py`, que precisa comparar modelos um a um.
  5. **O transporte Gemini não tem tempo limite** (`_gerar_gemini` não passa `http_options`/`timeout`). Em 28/09, o app v2 ficou mais de 8 min parado em "Etapa 2" com a Portaria 227 inteira.
- [x] (28/09) Branch publicada no GitHub (`da8ccd4`) e segundo app criado pelo Rodrigo: https://checklist-conformidade-v2.streamlit.app/.
- [ ] **App v2 instável com a Portaria 227 inteira na nuvem:** a 1ª tentativa teve JSON inválido do `gemini-3.5-flash-lite`; a 2ª deu 47 itens em cerca de 7,5 min, depois de 503 em toda a chave sem sufixo. Localmente: de 92 a 118 itens. Próximos passos (📝 propostas, aguardam ok): subir `_MAX_TOKENS` de 32768 para 65536 (o MVP não tinha teto); pôr na mensagem de erro de JSON qual modelo respondeu. 📝 A solução estrutural é a divisão em lotes (patch pausado).
- [x] (28/09) Push de `feat/llm-cadeia` e da tag `pre-llm-cadeia` ao GitLab.
- ~~Tirar `LLM_BASE_URL` dos *secrets* do v2~~: o Rodrigo decidiu manter os *secrets* iguais em todos os apps.
- [ ] Adaptar `tests/eval_modelos.py` ao `generate_checklist` novo (hoje ele passa `provider=`/`base_url=` e quebra). Depende do pedido 4.
- ~~Implantar o fluxo de versões `master` + `homologacao` + app "-v2"~~ (plano de 28/09): **superado pela D-C22** (`main` + `homologacao`, app `<app>-homologacao`, ordem de recriação na própria D-C22). Vira parte do passe por app.
- [ ] No passe por app: devolver `GEMINI_API_KEY` do app principal ao valor padrão (fim da exceção temporária de 28/09).
- [ ] 📝 Bug antigo, latente no `master`: `icon="←"` em `st.warning` levanta `StreamlitAPIException` no Streamlit 1.64 quando não há chave. A branch não tem mais esse aviso com ícone.
- [ ] Levar o trabalho da `feat/llm-cadeia` para produção **no passe por app** (D-C23), com o ok do Rodrigo; não há mais "merge no `master`" separado.
- [x] ~~**(sessão do buscador-normativos)** Criar o módulo comum de LLM para todos os MVPs~~ (feito na origem; adotado aqui em 28/09):
  - sequência LLM local → chave NUATI → chave Rodrigo → chave digitada pelo usuário (📝 sugestão: a do usuário primeiro, quando informada);
  - vários modelos por chave;
  - pular para a próxima opção em 429, 503, 404 e 400;
  - `thinking_budget` só para os modelos que aceitam;
  - mostrar qual opção atendeu;
  - avaliar Groq, Cerebras e OpenRouter (gratuitos) e Anthropic (chave paga com créditos).
  Depois, **trazer para cá**, integrando em `lib/llm.py` (`generate_checklist` / `_call_gemini`) e em `app.py` (`_render_sidebar`). Os fatos úteis estão em `LICOES.md`.
- [ ] Depois do módulo: retomar `pausado-2026-09-25-lotes-e-erros.patch` (divisão em lotes e mensagens de erro reais) com teste local da Portaria 227 antes de publicar. Sem os lotes, normativos grandes dependem de o `gemini-3.5-flash-lite` dar conta numa chamada só (deu conta da Portaria 227 em 75 s).
- [ ] 📝 App público: aviso na tela "não envie documentos internos ou com dados pessoais" (plano gratuito), ou voltar a deixá-lo privado. Decisão do Rodrigo.
- [x] (25/09) Commits enviados ao GitLab interno (`059591a`).

## P1: logo depois

- [ ] 📝 Candidato a funcionalidade da **v2.0** do app (ideia do Rodrigo, 23/09/2026): trazer para o app o que hoje só existe nos geradores de `gerador-checklists/`. O item abaixo é o ponto de partida.
- [ ] Incorporar no app os elementos do v1.08 que o app não tem:
  - colunas "Princípio / Tema" e "Precedência (decorrências)";
  - aba "Ações – Todos os Atores" (ator, fase, ação, artigo, texto literal, entregável, interação com);
  - "Resumo por Capítulo" e "Legenda e Instruções".
  - O v1.08 foi aprimorado por uma skill nunca incorporada ao app. Ver também `TODO-sync-gerador-nuati.md` e os scripts em `gerador-checklists/scripts/create_v108.py`.
- [ ] 📝 Prompt: instruir o modelo a usar como responsáveis só os papéis nomeados no normativo, com o nome oficial. O Gemma inventou "Gestor do sistema de IA"; o Sonnet e o Haiku erraram o nome da Ditec.

## P2: testes de modelo (pausados; roteiro em `tests/AVALIACAO_MODELOS.md`, seção 8)

- [ ] Definir os critérios de aceite **antes** da próxima rodada.
- [ ] Repetir as configurações candidatas de 3 a 5 vezes; testar o prompt com a lista de atores; fazer a validação humana às cegas de 20 a 30 itens; testar num segundo normativo (Roteiro SECIN 2018).
- [ ] Gemini em nível pago e Claude pela API, pelo pipeline do app (dependem de faturamento ou chave).

## P3: branding e outros apps

- [ ] (Rodrigo) Revisar `branding/README.md` (itens 📝).
- [ ] Aplicar `branding/` nos outros apps: DOU-clipping-app, pesquisa_diario, scopediagram, wiki-chat (HTML via `tokens.css`), auditflowmongodb (hoje com `nuati.css` próprio).
- [ ] Sincronizar com a metodologia completa de `gerador-checklists/` (`TODO-sync-gerador-nuati.md`).

## Feito

- [x] 2026-09-25: **MVP no ar funcionando** (confirmado pelo Rodrigo): `69f8c53` permite modelos "lite"; *secrets* com `GEMINI_MODEL = "gemini-3.5-flash-lite"` e a chave do Rodrigo; snapshot `090aa67` publicado no GitHub.

- [x] 2026-09-23: rodada 2 de testes (lotes de artigos × Gemma com e sem raciocínio × subagentes Opus, Sonnet e Haiku), registrada em `tests/AVALIACAO_MODELOS.md`. Commit `dcc3ca3`.
- [x] 2026-09-23: pesquisa do que é preciso para o Gemini funcionar (`DECISOES.md`).
- [x] 2026-09-23: dados internos movidos para `_sessao/INTERNO.md`; primeiro snapshot público publicado no GitHub via `scripts/publicar_github.sh` (sem `INTERNO.md`; o `gerador-checklists/` foi incluído num segundo snapshot, a pedido do Rodrigo). O Streamlit Cloud republicou; faltam os *secrets*.
- [x] 2026-09-23: commit `dcc3ca3` enviado ao `origin` (GitLab interno).
- [x] 2026-09-22: rodada 1 de testes (documento inteiro × por capítulo).
- [x] 2026-09-22: chave Gemini nova no `.env`, testada com o gemini-3.6-flash.
- [x] 2026-09-22: guia de identidade visual (`branding/`) criado e aplicado ao app (validado por screenshot local).
- [x] 2026-09-22: provider LLM local, allowlist anti-SSRF, terminologia oficial no prompt, README com a URL de deploy.
