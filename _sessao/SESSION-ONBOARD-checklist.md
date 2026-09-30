---
area: checklist
last_updated: 2026-09-30
related: [_sessao/TODO.md, _sessao/DECISOES.md, _sessao/LICOES.md, _sessao/SPEC.md, _sessao/log.md, _sessao/INFRASTRUCTURE-REFERENCE.md, _sessao/INTERNO.md, _sessao/pausado-2026-09-25-lotes-e-erros.patch, BLOCKED-ON-RODRIGO.md, tests/AVALIACAO_MODELOS.md, branding/README.md, scripts/publicar_github.sh, llm_cadeia/README.md, .claude/commands/onboard-checklist.md, ../framework/LEVANTAMENTO-FRAMEWORK.md, ../buscador-normativos/_DECISOES-PENDENTES.md]
---

# Estado: checklist-conformidade

**O que é:** app Streamlit que transforma normativos em checklists de conformidade (Excel). O essencial é extrair os dispositivos e atribuir os responsáveis ([SPEC](SPEC.md)).

**Repositórios:** `origin` = servidor git interno da Câmara (Gitea; histórico completo). `github` = **público** e **publica os apps** no Streamlit Cloud; recebe só snapshots, via `bash scripts/publicar_github.sh`, sem `_sessao/INTERNO.md`.

## Onde paramos (30/09/2026): passe por app, parado no passo 6 (Streamlit, com o Rodrigo)

Este é o **1º app a receber o `nuati-framework`**. Nesta rodada o framework (`29880aa`, branch `homologacao` de lá, antes da v0.1.0) entra **só na homologação**; o que for visto no ar volta para a sessão do framework como evidência para aprovar a v0.1.0. A produção não muda de código.

- ✅ Passos 0 a 5 feitos (detalhes no [log](log.md) de 30/09):
  - tags `pre-framework-2026-09-30-master` e `pre-framework-2026-09-30-feat-llm-cadeia` no interno;
  - `homologacao` (de `feat/llm-cadeia`) com `llm_cadeia` 1.1.0, `branding` 1.0.0, `extracao_texto` 1.0.0, `tempo_economizado` 1.0.0 e `publicar_snapshot` 1.0.0, um commit cada; 113 testes passam, 1 `xfail`;
  - `main` = `master` (`eab1039`, mesmo código do que está no ar);
  - GitHub (snapshots): `main` = `3709a25`, `homologacao` = `2233c9a`. As branches antigas de lá (`master` `090aa67`, `feat/llm-cadeia` `da8ccd4`) seguem alimentando os apps de hoje.
- ⏸ **Passo 6 é do Rodrigo** (receita em [BLOCKED-ON-RODRIGO](../BLOCKED-ON-RODRIGO.md)): recriar a produção na mesma URL na branch `main` e criar `checklist-conformidade-homologacao` na `homologacao`.
- Apps hoje: produção https://checklist-conformidade.streamlit.app/ (branch `master` do GitHub, até o passo 6); teste https://checklist-conformidade-v2.streamlit.app/ (`feat/llm-cadeia`; sai no passo 8, com o OK do Rodrigo).
- ⚠ Os *Secrets* da produção continuam com a exceção de 28/09 (não padronizar até a produção receber o framework).
- Publicar no GitHub: `bash publicar_snapshot/publicar_snapshot.sh [--simular] --ramo <branch>`. ⚠ Para publicar uma branch diferente da aberta, use um worktree ([LICOES](LICOES.md), 30/09).

## Branches e ponto de retorno

- `main` (produção) e `homologacao` (trabalho) no interno e no GitHub. `master` e `feat/llm-cadeia` ainda existem, até o passo 8.
- Tags de retorno: `pre-framework-2026-09-30-master` (`eab1039`), `pre-framework-2026-09-30-feat-llm-cadeia` (`0401040`) e a antiga `pre-llm-cadeia` (`eab1039`).

## Próximo passo

1. Rodrigo faz o passo 6 no Streamlit Cloud.
2. Passo 7: conferir os dois apps no ar, recurso por recurso ([TODO](TODO.md)).
3. Passo 8 (OK do Rodrigo): `main` padrão no GitHub; apagar branches velhas e o app `-v2`, com nova confirmação.
4. Passo 9: registro de cópias no README §4 do framework. Passo 10: fechar o journal.

## Decisões em aberto

- Deste app: [DECISOES](DECISOES.md), seção "Em aberto".
- Compartilhadas (framework, ambientes, apps públicos): `buscador-normativos/_DECISOES-PENDENTES.md` no `origin/master` atual de lá. Em 29/09, D-C22 a D-C26 estavam todas decididas; a D-C26 (apps públicos, faturamento desligado) toca a pergunta local sobre o app público.

## Ações que dependem do Rodrigo

[BLOCKED-ON-RODRIGO.md](../BLOCKED-ON-RODRIGO.md).

## Ponteiros

- Tarefas: [TODO](TODO.md) · Decisões: [DECISOES](DECISOES.md) · Pegadinhas: [LICOES](LICOES.md) · Linha do tempo: [log](log.md)
- Endereços, variáveis e receitas: [INFRASTRUCTURE-REFERENCE](INFRASTRUCTURE-REFERENCE.md) · Valores internos: `INTERNO.md` (só no servidor interno)
- Código: `app.py` · `lib/llm.py` · `lib/extractor.py` · `lib/prompt_templates.py` · `branding/streamlit_cd/cd_brand.py` · `llm_cadeia/` (congelada)
- Testes: `tests/eval_modelos.py` (quebrado pela branch, ver [TODO](TODO.md)), `tests/fixtures/`, `tests/resultados/`, `llm_cadeia/test_llm_cadeia.py`
- A incorporar (v2.0): `gerador-checklists/`, `TODO-sync-gerador-nuati.md`
- Snapshot na memória: `~/.claude/projects/C--Users-P-8106-Documents-solucoes-checklist-conformidade/memory/checklist_state_2026-09-29.md`
