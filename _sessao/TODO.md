# TODO — checklist-conformidade

<!-- last_audit: 2026-10-01 · itens concretos, mais urgentes no topo · ações que só o Rodrigo pode fazer: BLOCKED-ON-RODRIGO.md (raiz) -->

## ▶ App no servidor do Nuati (01/10)

- [x] (01/10) Scripts em `servidor/` (`instalar_tarefa.ps1`, `atualizar.ps1`, `iniciar.cmd`, `comum.ps1`, `README.md`), testados nesta máquina num worktree da `main` (tudo menos registrar a tarefa, que exige administrador): `.venv`, dependências, `iniciar.cmd`, health `ok`, parada pela porta.
- [x] (01/10, Rodrigo, no servidor) `git pull` no clone da `main`; criar o `.env` (nomes do `.env.example` da `main`: `LOCAL_LLM_URL`, `LOCAL_LLM_MODEL`, `LOCAL_LLM_DISABLE_THINKING=1`, `GEMINI_API_KEY`, `GEMINI_MODEL`); rodar `servidor\instalar_tarefa.ps1 -Porta 8401` como Administrador. Instalado: app no ar na 8401. Ver `BLOCKED-ON-RODRIGO.md`.
- [x] (01/10) Conferido no servidor: de outra máquina da rede, `/_stcore/health` = `ok` e página 200 (Claude); o Gemini gerou checklist (Rodrigo; tempo e itens não informados); o local estourou o tempo (item abaixo).
- [ ] **LLM local no servidor estoura o tempo (300 s)** (Rodrigo, 01/10; normativo usado não informado). O LM Studio está bem (chamada mínima em 0,75 s, 21,6 tokens/s, medido daqui em 01/10); o problema é a `main` mandar o normativo inteiro numa chamada (16 de 104 itens com a Portaria 227, `LICOES.md` 22/09). Aumentar o tempo não resolve: em 300 s, a 21,6 tokens/s, cabem uns 6.500 tokens de resposta (300 × 21,6), e um checklist completo da Portaria passa de 10.000 (📝 estimativa; a velocidade de 22/09 era 27,7 tokens/s, medida em outra condição). Caminho: a divisão em lotes (patch pausado, P0 abaixo). Fica para depois (Rodrigo).
- [x] (01/10) Relatório e guia para o framework absorver a implantação no servidor como recurso: `_sessao/relatorio-servidor-nuati-para-framework.md`. O Rodrigo leva à sessão do framework, que depois gera o prompt para o buscador.
- [ ] Publicar no GitHub os snapshots pendentes (`homologacao` publicada em 05/10, `1f617ff` = `ce9e708`; falta a `main`, sem a `servidor/`), com `--simular` antes e o ok do Rodrigo. Não afeta o servidor nem os apps.
- [ ] Quando o framework soltar o recurso (em 01/10 a sessão do framework já tinha um `servidor_nuati/` sem commit em `../nuati-framework`; reler antes de mexer na `servidor/` daqui): trocar a pasta `servidor/` daqui pela cópia do framework (regra §2 do README de lá) e atualizar o registro de cópias.

## ▶ Próximo trabalho (Rodrigo, 01/10): planilha de saída no padrão v1.08, já como v1.09

Na `homologacao`. Referência: `gerador-checklists/checklists/Checklist_Portaria_227_2025_IA_v1.08.xlsx`, gerada por `gerador-checklists/scripts/create_v108.py` (dados em `gerador-checklists/data/`); notas em `TODO-sync-gerador-nuati.md`. O código da planilha do app é `lib/excel_builder.py`.

- [x] (01/10) Levantar a diferença entre a planilha do app e a v1.08 (o Rodrigo citou, em 01/10): **colunas novas**, **abas novas** e **sem as linhas de separação de capítulo** (a planilha do app ainda as tem: conferido no Excel baixado da homologação em 01/10). Medido em 01/10 (`openpyxl` sobre os dois):
  - app (`lib/excel_builder.py`, `COLUMNS`): 2 abas ("Checklist de Conformidade", "Legenda"), 14 colunas, com linhas de capítulo;
  - v1.08: 5 abas ("Checklist Conformidade", "Curso IA Aplicada — SECIN", "Ações — Todos os Atores", "Resumo por Capítulo", "Legenda e Instruções"); a principal tem 18 colunas, entre elas "Princípio / Tema", "Criticidade (I×P)", "Nível de Risco MCGR" e "Precedência (decorrências)", sem linhas de capítulo e ordenada por criticidade;
  - a v1.08 não é gerada do zero: `create_v108.py` copia a v1.07 e a edita, que veio do `create_v107.py` sobre a v1.06 (`create_v106.py`); as abas "Ações" e "Curso" e a "Precedência" vêm de dados curados (`gerador-checklists/data/*.json`), não de LLM.
- [x] (01/10, decidido "1a 2a 3a 4a", ver `DECISOES.md`) 📝 Decisão a propor ao Rodrigo antes de codar: o que o app passa a gerar pelo LLM para **qualquer** normativo (colunas novas, abas "Ações", "Resumo por Capítulo") e o que fica específico da Portaria 227 (ex.: aba "Curso", dados curados). A metodologia MCGR usada na v1.08 tem como fonte `referencias/MCGR-Modelo-Corporativo-Gestao-Riscos-CD.{md,pdf}` (versionados em 01/10; documento público, Rodrigo).
- [x] (01/10, código na `homologacao`) **v1.09: separar os atores.** Hoje responsável e atores são campos multivalorados, o que dificulta o rastreamento (Rodrigo, 01/10). 📝 Desenho em aberto, a propor ao Rodrigo antes de codar: por exemplo, uma linha por par item × ator numa aba própria, ou colunas por ator.
- [x] (01/10) O que muda no prompt e na validação para o modelo devolver os campos novos (`lib/prompt_templates.py`, `lib/llm.py`).
- [x] (01/10) **Código da v1.09** na `homologacao`: prompt (campos `principio`, `precedencia`, `atores` com `papel`; o modelo não devolve mais `nivel`), `validate_items` (criticidade e nível pelo código; atores sem repetição, mesma grafia em todos os itens; `responsavel` = ator principal; aceita o `responsavel` antigo em texto), `build_excel` (17 colunas, ordem por criticidade, sem linhas de capítulo, abas Ações por Ator, Resumo por Capítulo e Legenda), prévia com I×P, `tests/eval_modelos.py` lendo os atores. Testes: `tests/test_planilha_v109.py`.
- [x] (05/10, ok do Rodrigo) Publicar a v1.09 no app de homologação: `github/homologacao` = `1f617ff` (snapshot de `ce9e708`).
- [x] (06/10) Ajuste pedido pelo Rodrigo depois do teste no ar: aba principal na ordem dos artigos, não por criticidade.
- [x] (06/10) **Conferência do texto literal com rodadas de correção** (`lib/conferencia.py`, `corrigir_literais` em `lib/llm.py`, coluna "Conferência do Texto Literal", etapa 3 de 4 e aviso na tela). Testes: `tests/test_conferencia_literal.py`. Decisão em `DECISOES.md` (06/10).
- [ ] 📝 Rodrigo: confirmar o limite de 3 rodadas e a tolerância da comparação (`DECISOES.md`, 06/10).
- [ ] 📝 A conferência estrita acha 4 divergências no texto **curado** da v1.08 (`gerador-checklists/data/checklist_conformidade_data.json`), contra `tests/fixtures/portaria_227_2025.txt`: itens 2 ("[...]"), 59 ("desde sua concepção" no lugar de "de sua concepção"), 72 (falta ", nos termos no Ato da Mesa nº 152...") e 97 (início diferente). A avaliação de 23/09 só apontava 2, com comparação tolerante. Material de auditoria: corrigir só com o ok do Rodrigo.
- [ ] **Rodrigo:** testar a v1.09 no ar (https://checklist-conformidade-homologacao.streamlit.app/) com a Portaria 227 inteira: 17 colunas e ordem por criticidade, aba Ações por Ator (filtrar por ator), Resumo, Legenda, acentos nos atores, tempo de geração.
- [ ] 📝 O código não junta plural e singular do mesmo ator ("Gestores de Negócio" e "Gestor de Negócio"): depende do prompt, que pede o singular. Visto ao passar os 104 itens curados da v1.08 (que têm as duas formas). Se o modelo também misturar, decidir se vale uma regra no código.
- [ ] 📝 Tempo economizado: as etapas manuais (`_ETAPAS_MANUAIS` em `app.py`, 9,0 min por item, validadas pelo Rodrigo) não contam princípio, precedência e atores. Rever só com o ok dele.
- A v1.08 foi feita **por iteração, sem skill** (Rodrigo, 01/10): o que ela tem está na própria planilha, no `create_v108.py` e nos dados de `gerador-checklists/data/`.

## ✅ Passe por app concluído (30/09-01/10): 1º app a receber o framework

Objetivo da rodada: o framework (`nuati-framework` @ `29880aa`, branch `homologacao` de lá) entra só na **homologação** deste app, e o que for visto no ar vira evidência para a v0.1.0 do framework. A **produção não recebe o framework** nesta rodada: a `main` nasceu do `master`, sem mudança de código.

- [x] (30/09) Passos 0 a 5: tags `pre-framework-2026-09-30-master` e `pre-framework-2026-09-30-feat-llm-cadeia` (interno); linha de base dos testes (números no `log.md` de 30/09); `homologacao` (de `feat/llm-cadeia`) com os 5 recursos adotados, um commit cada; `main` = `master` (`eab1039`); snapshots no GitHub `main` = `3709a25`, `homologacao` = `2233c9a`. Detalhes no `log.md` de 30/09.
- [x] (30/09) Passo 6 (Rodrigo): produção na `main` (mesma URL) e `checklist-conformidade-homologacao` na `homologacao`.
- [x] (01/10) Passo 7: os 5 recursos conferidos no ar e a produção igual a antes (`log.md`). O dropdown do tempo economizado foi validado pelo Rodrigo em 01/10.
- [ ] 📝 Limpeza do app: `use_container_width` está obsoleto no Streamlit 1.64 (avisos no log da nuvem); trocar por `width="stretch"`.
- [x] (01/10) Passo 8, com o OK do Rodrigo: `main` padrão no GitHub; apagados o app `-v2` (Rodrigo), `master` e `feat/llm-cadeia` no GitHub, `feat/llm-cadeia` e `master` no interno (depois que o Rodrigo trocou a padrão do Gitea para `main`) e as duas branches locais.
- [x] (01/10) Passo 9: registro de cópias no README §4 do framework (commit `975970b` na `homologacao` de lá).
- [ ] **Destravado em 01/10 (v0.1.0 aprovada, F-A3):** levar o framework para a produção (`homologacao` → `main` com tag, com o ok do Rodrigo), padronizando antes os *Secrets* da produção (fim da exceção de 28/09). ⚠ O servidor do Nuati também roda a `main`: antes do `atualizar.ps1`, reescrever o `.env` de lá com os nomes do `llm_cadeia` (`LLM_BASE_URL`, `LLM_MODEL`, `LLM_DISABLE_THINKING`, `GEMINI_API_KEY`, opcional `GEMINI_MODELS`; tabela "Segredos" de `llm_cadeia/README.md`, que o `.env.example` não cobre por inteiro), porque os nomes antigos (`LOCAL_LLM_*`, `GEMINI_MODEL`) deixam de ser lidos. Conferir também a F-A8 do framework (resposta vazia do `local`). ⚠ Na promoção, `git merge --ff-only` falha (a `main` tem os cherry-picks da `servidor/`): use merge normal, que sai limpo (`LICOES.md`, 01/10). Ordem: *Secrets* do Streamlit e `.env` do servidor antes; merge + tag; push no Gitea; snapshot `--ramo main`; `atualizar.ps1` no servidor; conferir os dois.
- [x] (01/10) **Pedido ao framework** (relatório do passe): `publicar_snapshot` 1.0.0 falhava ao publicar uma branch diferente da aberta. **Corrigido lá na 1.0.1** (`nuati-framework` `56d7eb0`, `-f` no `git rm --cached`; teste novo).
- [x] (01/10, sessão da tarde: cópia 1.0.0 igual a `29880aa` por hash, 5/5; 1.0.1 copiada de `56d7eb0`, hashes 5/5; 9 testes passam) **Recopiar o `publicar_snapshot` 1.0.1** na `homologacao`: conferir antes a cópia 1.0.0 por hash contra `29880aa` (regra §2.3 do README do framework), copiar a pasta inteira de `56d7eb0` por `git archive`, rodar `py -m pytest publicar_snapshot -q`, commit "adota publicar_snapshot 1.0.1 (nuati-framework @ 56d7eb0)", e atualizar a linha do checklist no README §4 do framework. Depois disso, o contorno do worktree (`LICOES.md`, 30/09) deixa de ser necessário.

## P0: módulo comum de provedores e chaves de LLM (a partir de 25/09/2026)

- [x] (28/09) `llm_cadeia` 1.0.0 (buscador @ `3edba4d`) adotado na branch `feat/llm-cadeia`. Tag `pre-llm-cadeia` marca a versão no ar. Detalhes no `log.md` de 28/09.
- [x] (30/09) **Pedidos para a origem (sessão do framework, D-C24): os 5 resolvidos no `llm_cadeia` 1.1.0**, adotado na `homologacao` (1: `LLM_TIMEOUT_S`, padrão 300 s; 2: `LLM_DISABLE_THINKING`; 3: pasta sem dado interno, e a trava do snapshot passou sem exceção; 4: `LLM_SOMENTE`; 5: 120 s no Gemini). Histórico dos pedidos:
  1. **Tempo limite do LLM local de 120 s é curto** (`nucleo.py`, `timeout=(5, 120)`). Medido em 28/09, trecho de 5.000 caracteres da Portaria 227 com o prompt do app: 154 s com raciocínio (como o módulo envia), 54 s sem. Resultado: o `local` nunca atende um normativo real, e a cadeia passa para o Gemini. O app antigo usava 300 s.
  2. **Não há como desligar o raciocínio do Gemma** (`chat_template_kwargs: {enable_thinking: false}`; no app antigo, `LOCAL_LLM_DISABLE_THINKING=1`). Sem ele, a mesma chamada cai de 154 s para 54 s.
  3. **A pasta tem dados internos** (IP do servidor local e login da conta Google) no `README.md`, no `nucleo.py` (docstring e comentário) e no `test_llm_cadeia.py`. 📝 Continua valendo como higiene na origem, mas **não bloqueia mais**: em 28/09, o Rodrigo decidiu publicar assim mesmo (exceção na trava; ver `DECISOES.md`).
  4. 📝 Não há como forçar um só provedor num teste: `_segredo` lê `st.secrets` antes das variáveis de ambiente, e o `st.secrets` carrega o `~/.streamlit/secrets.toml` global mesmo fora do `streamlit run`. O `LLM_ORDEM` só reordena. Isso afeta o `tests/eval_modelos.py`, que precisa comparar modelos um a um.
  5. **O transporte Gemini não tem tempo limite** (`_gerar_gemini` não passa `http_options`/`timeout`). Em 28/09, o app v2 ficou mais de 8 min parado em "Etapa 2" com a Portaria 227 inteira.
- [x] (28/09) Branch publicada no GitHub (`da8ccd4`) e segundo app criado pelo Rodrigo: https://checklist-conformidade-v2.streamlit.app/.
- [ ] **App v2 instável com a Portaria 227 inteira na nuvem** (01/10: no app de homologação, a URL da Portaria inteira gerou 83 itens em cerca de 1 min 15 s, numa execução só; não basta para dar por resolvido): a 1ª tentativa teve JSON inválido do `gemini-3.5-flash-lite`; a 2ª deu 47 itens em cerca de 7,5 min, depois de 503 em toda a chave sem sufixo. Localmente: de 92 a 118 itens. Próximos passos (📝 propostas, aguardam ok): subir `_MAX_TOKENS` de 32768 para 65536 (o MVP não tinha teto); pôr na mensagem de erro de JSON qual modelo respondeu. 📝 A solução estrutural é a divisão em lotes (patch pausado).
- [x] (28/09) Push de `feat/llm-cadeia` e da tag `pre-llm-cadeia` ao GitLab.
- ~~Tirar `LLM_BASE_URL` dos *secrets* do v2~~: o Rodrigo decidiu manter os *secrets* iguais em todos os apps.
- [x] (30/09) `tests/eval_modelos.py` adaptado ao `generate_checklist` novo, com `LLM_SOMENTE`/`LLM_DISABLE_THINKING` por modelo e registro de quem respondeu (commit `2075aa1`).
- ~~Implantar o fluxo de versões `master` + `homologacao` + app "-v2"~~ (plano de 28/09): **superado pela D-C22** (`main` + `homologacao`, app `<app>-homologacao`, ordem de recriação na própria D-C22). Vira parte do passe por app.
- [ ] Quando a produção receber o framework (depois da v0.1.0): devolver `GEMINI_API_KEY` da produção ao valor padrão (fim da exceção temporária de 28/09).
- [x] (30/09) Bug do `icon="←"` em `st.warning` (StreamlitAPIException "not a valid emoji" quando nenhum provedor está configurado): **corrigido na `homologacao`** (ícone 👈). A anotação anterior, de que a branch não tinha mais o aviso, estava errada: apareceu no app de homologação em 30/09. ⚠ Continua latente na `main` (produção); vai junto quando a produção receber o framework.
- ~~Levar o trabalho da `feat/llm-cadeia` para produção no passe por app~~ (01/10): a homologação recebeu no passe; a produção vai depois da v0.1.0 (item na seção do passe por app, acima).
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
  - O v1.08 foi aprimorado por iteração, sem skill (Rodrigo, 01/10), e nunca foi incorporado ao app. Ver também `TODO-sync-gerador-nuati.md` e os scripts em `gerador-checklists/scripts/create_v108.py`.
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
