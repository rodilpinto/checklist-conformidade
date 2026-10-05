---
area: checklist
last_updated: 2026-10-01
related: [_sessao/TODO.md, _sessao/DECISOES.md, _sessao/LICOES.md, _sessao/SPEC.md, _sessao/log.md, _sessao/INFRASTRUCTURE-REFERENCE.md, _sessao/INTERNO.md, _sessao/pausado-2026-09-25-lotes-e-erros.patch, _sessao/relatorio-servidor-nuati-para-framework.md, servidor/README.md, BLOCKED-ON-RODRIGO.md, tests/AVALIACAO_MODELOS.md, branding/README.md, publicar_snapshot/README.md, publicar_snapshot.conf, llm_cadeia/README.md, lib/excel_builder.py, gerador-checklists/scripts/create_v108.py, TODO-sync-gerador-nuati.md, .claude/commands/onboard-checklist.md, ../nuati-framework/README.md, ../nuati-framework/DECISOES.md, ../buscador-normativos/_DECISOES-PENDENTES.md]
---

# Estado: checklist-conformidade

**O que é:** app Streamlit que transforma normativos em checklists de conformidade (Excel). O essencial é extrair os dispositivos e atribuir os responsáveis ([SPEC](SPEC.md)).

**Repositórios:** `origin` = servidor git interno da Câmara (Gitea; histórico completo). `github` = **público** e **publica os apps** no Streamlit Cloud; recebe só snapshots, via `bash publicar_snapshot/publicar_snapshot.sh --ramo <branch>`, sem `_sessao/INTERNO.md` nem `publicar_snapshot.conf`. O **servidor do Nuati** puxa a `main` do Gitea (manual, ver abaixo).

## Onde paramos (01/10/2026): app no servidor do Nuati; framework só na homologação

- **Produção (Streamlit):** https://checklist-conformidade.streamlit.app/ na branch `main` (GitHub `3709a25`). Código antigo, **sem framework**; *Secrets* com a exceção de 28/09 (não padronizar até a produção receber o framework).
- **Produção (servidor do Nuati, novo em 01/10):** tarefa agendada do Windows na porta 8401, mesma `main` (interno: `eab1039` + só a pasta `servidor/` e duas linhas em `.gitignore`/`.gitattributes`, por cherry-pick: na promoção, merge normal, não `--ff-only`, ver `LICOES.md`). Servidor, pasta e `.env` (LM Studio + Gemini): `INTERNO.md`. Gemini gerou checklist lá; o **LLM local estoura 300 s** com normativo inteiro (chamada única; [TODO](TODO.md)). **Atualizar é manual:** a cada push da `main` no Gitea, o Rodrigo roda `servidor\atualizar.ps1` no servidor ([servidor/README](../servidor/README.md)).
- **Homologação:** https://checklist-conformidade-homologacao.streamlit.app/ na branch `homologacao`, com o framework @ `29880aa` (versões das pastas: `__version__`/`CHANGELOG.md` de cada uma; registro no README §4 do framework). Os 5 recursos conferidos no ar (log de 30/09 e 01/10). A `servidor/` ainda não está no snapshot do GitHub (não faz falta).
- **Relatório para o framework** absorver a implantação no servidor como recurso: [relatorio-servidor-nuati-para-framework](relatorio-servidor-nuati-para-framework.md). O Rodrigo leva à sessão do framework, que depois gera o prompt para o buscador. Em 01/10 a sessão do framework já tinha um `servidor_nuati/` **sem commit** em `../nuati-framework` (`git -C ../nuati-framework status -s`).
- **Framework, conferido em 01/10 no fim desta sessão:** a **v0.1.0 foi aprovada** (F-A3, tag `v0.1.0` na `main` de lá) e o buscador já levou o framework à produção dele. Isso destrava o item 3 abaixo.

## Branches e ponto de retorno

- `main` (produção) e `homologacao` (trabalho), no interno e no GitHub (padrão `main` nos dois).
- Tags de retorno (interno): `pre-framework-2026-09-30-master` (`eab1039`, mensagem *"estado antes da migracao D-C22"*), `pre-framework-2026-09-30-feat-llm-cadeia` (`0401040`, mesma mensagem) e a antiga `pre-llm-cadeia` (`eab1039`). Voltar: `git switch -c volta <tag>`.
- Cadeia desta sessão: `homologacao` `13bc7dc` → `12d1592` → `9be45e2` → `561c166` → `e06b826`; `main` `8de4e7b` → `764f567` (cherry-pick só da `servidor/`). O SHA mais novo listado aqui está sempre um ou mais atrás dos commits que guardaram este arquivo; a cadeia real termina em `git log --oneline -3 <branch>`. Pontas no GitHub: `git ls-remote github`.

## Próximo passo

1. **Próximo trabalho neste app (Rodrigo, 01/10): planilha de saída no padrão v1.08, já como v1.09** (atores separados). Na `homologacao`. Itens, medições e a decisão a propor antes de codar: [TODO](TODO.md), seção do próximo trabalho.
2. ~~Recopiar o `publicar_snapshot` 1.0.1~~ (feito em 01/10, na `homologacao`). ⚠ A tag `pre-v109` marca o último ponto da `homologacao` antes do código da v1.09: na promoção do framework à produção (item 3), leve à `main` essa tag, não a ponta da branch, se a v1.09 ainda não estiver pronta.
3. **Destravado (v0.1.0 aprovada):** levar o framework para a produção (`homologacao` → `main` com tag, com o ok do Rodrigo). Antes: padronizar os *Secrets* do Streamlit de produção **e reescrever o `.env` do servidor com os nomes do `llm_cadeia`** (tabela "Segredos" de `llm_cadeia/README.md`); depois, `atualizar.ps1` no servidor. Itens no [TODO](TODO.md).
4. LLM local no servidor (e normativos grandes em geral): divisão em lotes (patch pausado, P0). Para depois (Rodrigo, 01/10).

## Decisões em aberto

- Deste app: [DECISOES](DECISOES.md), seção "Em aberto".
- Compartilhadas (leia sempre a versão do servidor; receita no passo 4 do onboard): `buscador-normativos/_DECISOES-PENDENTES.md` (`origin/main` de lá; o `master` foi apagado no passe do buscador) e `nuati-framework/DECISOES.md` (`origin/homologacao`; em 01/10: F-A3 decidida, abertas F-A4, F-A6 e os pedidos do buscador F-A7 a F-A10; a F-A8, resposta vazia do `local`, toca o servidor do Nuati).

## Ações que dependem do Rodrigo

[BLOCKED-ON-RODRIGO.md](../BLOCKED-ON-RODRIGO.md).

## Ponteiros

- Tarefas: [TODO](TODO.md) · Decisões: [DECISOES](DECISOES.md) · Pegadinhas: [LICOES](LICOES.md) · Linha do tempo: [log](log.md)
- Endereços, variáveis e receitas: [INFRASTRUCTURE-REFERENCE](INFRASTRUCTURE-REFERENCE.md) · Valores internos: `INTERNO.md` (só no servidor interno)
- Código do app: `app.py` · `lib/llm.py` · `lib/prompt_templates.py` · `lib/excel_builder.py` (planilha de saída) · `servidor/` (implantação no servidor do Nuati; candidata a recurso do framework). Pastas do framework, que **não se editam** (defeito vira pedido ao framework): `llm_cadeia/`, `branding/`, `extracao_texto/`, `tempo_economizado/`, `publicar_snapshot/`.
- Testes: `py -m pytest -q` da raiz (resultado medido em `log.md`); avaliação de modelos em `tests/eval_modelos.py` (com `LLM_SOMENTE`), `tests/fixtures/`, `tests/resultados/`
- A incorporar (v2.0): `gerador-checklists/`, `TODO-sync-gerador-nuati.md`
- Snapshot na memória: `~/.claude/projects/C--Users-P-8106-Documents-solucoes-checklist-conformidade/memory/checklist_state_2026-10-01.md`
