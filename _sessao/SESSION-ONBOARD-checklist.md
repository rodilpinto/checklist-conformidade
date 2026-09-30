---
area: checklist
last_updated: 2026-09-25
related: [_sessao/TODO.md, _sessao/DECISOES.md, _sessao/LICOES.md, _sessao/SPEC.md, _sessao/log.md, _sessao/INFRASTRUCTURE-REFERENCE.md, _sessao/INTERNO.md, _sessao/pausado-2026-09-25-lotes-e-erros.patch, BLOCKED-ON-RODRIGO.md, tests/AVALIACAO_MODELOS.md, branding/README.md, scripts/publicar_github.sh, .claude/commands/onboard-checklist.md]
---

# Estado: checklist-conformidade

**O que é:** app Streamlit que transforma normativos em checklists de conformidade (Excel). O essencial é extrair os dispositivos e atribuir os responsáveis ([SPEC](SPEC.md)).

**Repositórios:** o `origin` (GitLab interno) tem o histórico completo. O `github` (**público**, e **publica o app** no Streamlit Cloud) recebe só snapshots, via `bash scripts/publicar_github.sh`, sem `_sessao/INTERNO.md`. Confira o estado real com `git log --oneline -3` e `git status -sb`.

## Onde paramos (25/09/2026)

- ✅ **MVP no ar e funcionando** (confirmado pelo Rodrigo em 25/09): https://checklist-conformidade.streamlit.app/ (agora **público**), com Gemini `gemini-3.5-flash-lite` e a chave gratuita do Rodrigo nos *secrets*. A correção que permitiu isso é o commit `69f8c53`: modelos "lite" não recebem `thinking_budget`.
- **Feito antes:** provider Gemini ou Gemma local; `branding/`; anti-SSRF; terminologia oficial; testes de modelo exploratórios ([AVALIACAO_MODELOS](../tests/AVALIACAO_MODELOS.md)); dados internos isolados em `INTERNO.md`.
- **Pausado por decisão do Rodrigo, para evitar regressão:** a divisão em lotes (`lib/lotes.py`) e as mensagens de erro reais. Estão em [`pausado-2026-09-25-lotes-e-erros.patch`](pausado-2026-09-25-lotes-e-erros.patch); para retomar, `git apply --ignore-whitespace <patch>` e revisar o `lib/llm.py`, que mudou depois (`69f8c53`).

## Próximo passo

**Módulo comum de provedores e chaves de LLM, para todos os MVPs** (buscador, checklist, scopediagram e outros). A sequência será: LLM local → chave NUATI → chave Rodrigo → chave digitada pelo usuário, com vários modelos por chave e outros provedores gratuitos (Groq, Cerebras, OpenRouter) em estudo. **Vai ser desenvolvido primeiro numa sessão do buscador-normativos e depois trazido para cá** (decisão do Rodrigo, 25/09). Aqui, a integração é no `lib/llm.py` (`generate_checklist` / `_call_gemini`) e em `app.py` (`_render_sidebar`). Fatos úteis para o módulo: [LICOES](LICOES.md).

## Decisões em aberto (detalhes em [DECISOES](DECISOES.md#em-aberto-só-o-rodrigo-decide))

- Faturamento do Gemini ou uso da chave paga da Anthropic (o Rodrigo tem créditos).
- App público: incluir o aviso "não envie documentos internos" (plano gratuito) ou voltar a deixá-lo privado?
- Revisão e conformidade do `branding/` (Comid; grafia das unidades).

## Ações que dependem do Rodrigo

Ver [BLOCKED-ON-RODRIGO.md](../BLOCKED-ON-RODRIGO.md).

## Ponteiros

- Tarefas: [TODO](TODO.md) · Decisões: [DECISOES](DECISOES.md) · Pegadinhas: [LICOES](LICOES.md) · Linha do tempo: [log](log.md)
- Endereços, variáveis e receitas: [INFRASTRUCTURE-REFERENCE](INFRASTRUCTURE-REFERENCE.md) · Valores internos: `INTERNO.md` (só no GitLab)
- Código: `app.py` · `lib/llm.py` · `lib/extractor.py` · `lib/prompt_templates.py` · `branding/streamlit_cd/cd_brand.py`
- Testes: `tests/eval_modelos.py`, `tests/fixtures/`, `tests/resultados/`
- A incorporar (v2.0): `gerador-checklists/`, `TODO-sync-gerador-nuati.md`
- Snapshot na memória: `~/.claude/projects/C--Users-P-8106-Documents-solucoes-checklist-conformidade/memory/checklist_state_2026-09-25.md`
