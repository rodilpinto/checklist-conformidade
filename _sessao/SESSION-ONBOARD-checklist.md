---
area: checklist
last_updated: 2026-09-29
related: [_sessao/TODO.md, _sessao/DECISOES.md, _sessao/LICOES.md, _sessao/SPEC.md, _sessao/log.md, _sessao/INFRASTRUCTURE-REFERENCE.md, _sessao/INTERNO.md, _sessao/pausado-2026-09-25-lotes-e-erros.patch, BLOCKED-ON-RODRIGO.md, tests/AVALIACAO_MODELOS.md, branding/README.md, scripts/publicar_github.sh, llm_cadeia/README.md, .claude/commands/onboard-checklist.md, ../framework/LEVANTAMENTO-FRAMEWORK.md, ../buscador-normativos/_DECISOES-PENDENTES.md]
---

# Estado: checklist-conformidade

**O que é:** app Streamlit que transforma normativos em checklists de conformidade (Excel). O essencial é extrair os dispositivos e atribuir os responsáveis ([SPEC](SPEC.md)).

**Repositórios:** `origin` = servidor git interno da Câmara (Gitea; histórico completo). `github` = **público** e **publica os apps** no Streamlit Cloud; recebe só snapshots, via `bash scripts/publicar_github.sh`, sem `_sessao/INTERNO.md`.

## Onde paramos (29/09/2026): em pausa para o framework central

- ⏸ **Pausa pedida pelo Rodrigo** (decisões D-C22, D-C23 e D-C24, no ledger compartilhado `buscador-normativos/_DECISOES-PENDENTES.md`; ele é escrito por outras sessões ao mesmo tempo, então **leia sempre o `origin/master` atual de lá**, receita no passo 4 do `/onboard-checklist`). O framework vira o repositório privado `rodilpinto/nuati-framework`, origem única do que é comum. Depois, **um passe por app** adota o framework **e** migra para `main` (estável) + `homologacao` (playground). **Nada a fazer aqui até esse passe.**
- 🧊 **`llm_cadeia/` congelada** (D-C24): cópia 1.0.0 (buscador @ `3edba4d`), que não serve de fonte. Defeito achado vira pedido à sessão do framework ([TODO](TODO.md), P0).
- **App principal** (https://checklist-conformidade.streamlit.app/): segue `github/master` = `090aa67` (snapshot de 25/09) e funciona (92 itens com a Portaria 227 inteira, testado em 28/09 depois do incidente). ⚠ **Os *secrets* dele têm uma exceção temporária** (chave `_2` em `GEMINI_API_KEY` e `GEMINI_MODEL`); não os padronize antes do passe por app ([DECISOES](DECISOES.md), 28/09).
- **App de teste** (https://checklist-conformidade-v2.streamlit.app/): segue `github/feat/llm-cadeia` = `da8ccd4`. Funciona com texto curto e está instável com a Portaria inteira ([TODO](TODO.md), P0). Pela D-C22, vai ser recriado como `<app>-homologacao` no passe.
- **Pausado desde 25/09**, por decisão do Rodrigo: divisão em lotes e mensagens de erro reais, em [`pausado-2026-09-25-lotes-e-erros.patch`](pausado-2026-09-25-lotes-e-erros.patch).

## Branches e ponto de retorno

- `master` = `eab1039`, intocado desde 25/09. Tag de retorno `pre-llm-cadeia`, cuja mensagem é *"antes do llm_cadeia: versao do MVP no ar (Streamlit Cloud, github/master)"*. Para voltar: `git switch -c volta pre-llm-cadeia`.
- `feat/llm-cadeia` (trabalho de 28 e 29/09): cadeia desta sessão `2357a2e` → `e20febf` → `8cca21f` → `f676a17` → `a6df684` → `92ac158`, mais o commit deste checkpoint. O SHA mais novo listado aqui fica sempre um atrás do commit que guardou este arquivo; a cadeia real termina em `git log --oneline -3`.

## Próximo passo

Aguardar a sessão nova do framework e, depois, o **passe por app** (D-C23). O insumo que esta sessão deixou para ela é [`solucoes/framework/LEVANTAMENTO-FRAMEWORK.md`](../../framework/LEVANTAMENTO-FRAMEWORK.md) (repositório `Nuati-SECIN/framework`, que pela D-C25 vira espelho interno do novo). No passe, este app precisa de: `llm_cadeia` 1.0.1 ou superior vinda do framework; fim da exceção nos *secrets* do principal; recriação dos apps pela ordem da D-C22; e as propostas pendentes do v2 ([TODO](TODO.md), P0).

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
