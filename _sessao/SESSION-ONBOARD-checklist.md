---
area: checklist
last_updated: 2026-10-01
related: [_sessao/TODO.md, _sessao/DECISOES.md, _sessao/LICOES.md, _sessao/SPEC.md, _sessao/log.md, _sessao/INFRASTRUCTURE-REFERENCE.md, _sessao/INTERNO.md, _sessao/pausado-2026-09-25-lotes-e-erros.patch, BLOCKED-ON-RODRIGO.md, tests/AVALIACAO_MODELOS.md, branding/README.md, publicar_snapshot/README.md, publicar_snapshot.conf, llm_cadeia/README.md, lib/excel_builder.py, gerador-checklists/scripts/create_v108.py, TODO-sync-gerador-nuati.md, .claude/commands/onboard-checklist.md, ../nuati-framework/README.md, ../nuati-framework/DECISOES.md, ../buscador-normativos/_DECISOES-PENDENTES.md]
---

# Estado: checklist-conformidade

**O que é:** app Streamlit que transforma normativos em checklists de conformidade (Excel). O essencial é extrair os dispositivos e atribuir os responsáveis ([SPEC](SPEC.md)).

**Repositórios:** `origin` = servidor git interno da Câmara (Gitea; histórico completo). `github` = **público** e **publica os apps** no Streamlit Cloud; recebe só snapshots, via `bash publicar_snapshot/publicar_snapshot.sh --ramo <branch>`, sem `_sessao/INTERNO.md` nem `publicar_snapshot.conf`.

## Onde paramos (01/10/2026): passe por app concluído (1ª rodada, só homologação)

Este foi o **1º app a receber o `nuati-framework`**. O framework (`29880aa`, branch `homologacao` de lá, antes da v0.1.0) está **só na homologação**; a produção segue com o código antigo até a v0.1.0 do framework ser aprovada. Evidência de cada recurso no ar: [log](log.md) de 30/09.

- **Produção:** https://checklist-conformidade.streamlit.app/ na branch `main` (interno `eab1039`; GitHub `3709a25`, padrão do GitHub). Igual a antes; *Secrets* com a exceção de 28/09 (não padronizar até a produção receber o framework).
- **Homologação:** https://checklist-conformidade-homologacao.streamlit.app/ na branch `homologacao` (`llm_cadeia` 1.1.0, `branding` 1.0.0, `extracao_texto` 1.0.0, `tempo_economizado` 1.0.0, `publicar_snapshot` 1.0.0). Os 5 recursos conferidos no ar; o dropdown do tempo economizado validado pelo Rodrigo (01/10).
- **Limpeza (passo 8):** apagados o app `-v2`, `master` e `feat/llm-cadeia` no GitHub e `feat/llm-cadeia` e `master` no interno (depois que o Rodrigo trocou a branch padrão do Gitea para `main`) e localmente.
- **Registro de cópias** no README §4 do framework atualizado (commit `975970b` na `homologacao` de lá).
- Publicar no GitHub: `bash publicar_snapshot/publicar_snapshot.sh [--simular] --ramo <branch>`. ⚠ A cópia daqui é a 1.0.0: para publicar uma branch diferente da aberta, use um worktree ([LICOES](LICOES.md), 30/09) até recopiar a 1.0.1, que corrige isso ([TODO](TODO.md)).

## Branches e ponto de retorno

- `main` (produção) e `homologacao` (trabalho), no interno e no GitHub (padrão `main` nos dois).
- Tags de retorno (interno): `pre-framework-2026-09-30-master` (`eab1039`, mensagem *"estado antes da migracao D-C22"*), `pre-framework-2026-09-30-feat-llm-cadeia` (`0401040`, mesma mensagem) e a antiga `pre-llm-cadeia` (`eab1039`). Voltar: `git switch -c volta <tag>`.
- Cadeia desta sessão na `homologacao` (interno): `2075aa1` → `f84d7e9` → `aff5294` → `9c19a60` → `3dfd59e` → `9a8f468` → `1598bf1` → `c548ee8` → `d812e13`, mais os commits deste checkpoint. O SHA mais novo listado aqui está sempre um ou mais atrás dos commits que guardaram este arquivo; a cadeia real termina em `git log --oneline -3`. As pontas no GitHub (snapshots, histórico próprio): `git ls-remote github`.

## Próximo passo

1. **Próximo trabalho neste app (Rodrigo, 01/10): planilha de saída no padrão v1.08, já como v1.09.** Na `homologacao`. A v1.08 (`gerador-checklists/checklists/Checklist_Portaria_227_2025_IA_v1.08.xlsx`, feita por iteração, sem skill; gerada por `gerador-checklists/scripts/create_v108.py`) tem colunas novas e abas novas, e não tem as linhas de separação de capítulo que a planilha do app ainda tem. A v1.09 acrescenta a **separação de atores**: hoje responsável e atores são campos multivalorados, o que dificulta o rastreamento. Detalhes e itens: [TODO](TODO.md), seção do próximo trabalho.
2. Neste app, antes ou junto da planilha: recopiar o `publicar_snapshot` 1.0.1 do framework (`56d7eb0`, 01/10: corrige o pedido 6.1), conferindo antes a cópia 1.0.0 por hash (regra §2.3 do README do framework).
3. Outra sessão (framework): aprovar a v0.1.0 (F-A3) com a evidência deste passe (relatório entregue pelo Rodrigo em 01/10).
4. Depois da v0.1.0: levar o framework para a produção (`homologacao` → `main` com tag, *Secrets* da produção padronizados antes) e retomar o P0 (patch dos lotes, `_MAX_TOKENS`).

## Decisões em aberto

- Deste app: [DECISOES](DECISOES.md), seção "Em aberto".
- Compartilhadas: `buscador-normativos/_DECISOES-PENDENTES.md` (`origin/master` de lá; D-C22 a D-C26 decididas, a última em 29/09, conferido em 01/10; a D-C26 toca a pergunta local sobre o app público) e `nuati-framework/DECISOES.md` (`origin/homologacao` de lá; em 01/10, abertas F-A3 = promover a v0.1.0, que depende da evidência deste passe, F-A4 e F-A6). Leia sempre a versão do servidor (receita no passo 4 do onboard).

## Ações que dependem do Rodrigo

[BLOCKED-ON-RODRIGO.md](../BLOCKED-ON-RODRIGO.md).

## Ponteiros

- Tarefas: [TODO](TODO.md) · Decisões: [DECISOES](DECISOES.md) · Pegadinhas: [LICOES](LICOES.md) · Linha do tempo: [log](log.md)
- Endereços, variáveis e receitas: [INFRASTRUCTURE-REFERENCE](INFRASTRUCTURE-REFERENCE.md) · Valores internos: `INTERNO.md` (só no servidor interno)
- Código do app: `app.py` · `lib/llm.py` · `lib/prompt_templates.py` · `lib/excel_builder.py` (planilha de saída). Pastas do framework, que **não se editam** (defeito vira pedido ao framework): `llm_cadeia/`, `branding/`, `extracao_texto/`, `tempo_economizado/`, `publicar_snapshot/`.
- Testes: `py -m pytest -q` da raiz (resultado medido em `log.md`); avaliação de modelos em `tests/eval_modelos.py` (com `LLM_SOMENTE`), `tests/fixtures/`, `tests/resultados/`
- A incorporar (v2.0): `gerador-checklists/`, `TODO-sync-gerador-nuati.md`
- Snapshot na memória: `~/.claude/projects/C--Users-P-8106-Documents-solucoes-checklist-conformidade/memory/checklist_state_2026-10-01.md`
