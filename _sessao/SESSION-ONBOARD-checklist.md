---
area: checklist
last_updated: 2026-10-01
related: [_sessao/TODO.md, _sessao/DECISOES.md, _sessao/LICOES.md, _sessao/SPEC.md, _sessao/log.md, _sessao/INFRASTRUCTURE-REFERENCE.md, _sessao/INTERNO.md, _sessao/pausado-2026-09-25-lotes-e-erros.patch, BLOCKED-ON-RODRIGO.md, tests/AVALIACAO_MODELOS.md, branding/README.md, scripts/publicar_github.sh, llm_cadeia/README.md, .claude/commands/onboard-checklist.md, ../framework/LEVANTAMENTO-FRAMEWORK.md, ../buscador-normativos/_DECISOES-PENDENTES.md]
---

# Estado: checklist-conformidade

**O que é:** app Streamlit que transforma normativos em checklists de conformidade (Excel). O essencial é extrair os dispositivos e atribuir os responsáveis ([SPEC](SPEC.md)).

**Repositórios:** `origin` = servidor git interno da Câmara (Gitea; histórico completo). `github` = **público** e **publica os apps** no Streamlit Cloud; recebe só snapshots, via `bash scripts/publicar_github.sh`, sem `_sessao/INTERNO.md`.

## Onde paramos (01/10/2026): passe por app concluído (1ª rodada, só homologação)

Este foi o **1º app a receber o `nuati-framework`**. O framework (`29880aa`, branch `homologacao` de lá, antes da v0.1.0) está **só na homologação**; a produção segue com o código antigo até a v0.1.0 do framework ser aprovada. Evidência de cada recurso no ar: [log](log.md) de 30/09.

- **Produção:** https://checklist-conformidade.streamlit.app/ na branch `main` (interno `eab1039`; GitHub `3709a25`, padrão do GitHub). Igual a antes; *Secrets* com a exceção de 28/09 (não padronizar até a produção receber o framework).
- **Homologação:** https://checklist-conformidade-homologacao.streamlit.app/ na branch `homologacao` (`llm_cadeia` 1.1.0, `branding` 1.0.0, `extracao_texto` 1.0.0, `tempo_economizado` 1.0.0, `publicar_snapshot` 1.0.0). Os 5 recursos conferidos no ar; o dropdown do tempo economizado validado pelo Rodrigo (01/10).
- **Limpeza (passo 8):** apagados o app `-v2`, `master` e `feat/llm-cadeia` no GitHub e `feat/llm-cadeia` e `master` no interno (depois que o Rodrigo trocou a branch padrão do Gitea para `main`) e localmente.
- **Registro de cópias** no README §4 do framework atualizado (commit `975970b` na `homologacao` de lá).
- Publicar no GitHub: `bash publicar_snapshot/publicar_snapshot.sh [--simular] --ramo <branch>`. ⚠ Para publicar uma branch diferente da aberta, use um worktree ([LICOES](LICOES.md), 30/09).

## Branches e ponto de retorno

- `main` (produção) e `homologacao` (trabalho), no interno e no GitHub (padrão `main` nos dois).
- Tags de retorno (interno): `pre-framework-2026-09-30-master` (`eab1039`), `pre-framework-2026-09-30-feat-llm-cadeia` (`0401040`) e a antiga `pre-llm-cadeia` (`eab1039`).

## Próximo passo

1. Sessão do framework: aprovar a v0.1.0 com a evidência deste passe e corrigir o defeito do `publicar_snapshot` ([TODO](TODO.md)).
2. Depois da v0.1.0: levar o framework para a produção (`homologacao` → `main` com tag, *Secrets* da produção padronizados antes) e retomar o P0 (patch dos lotes, `_MAX_TOKENS`).

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
