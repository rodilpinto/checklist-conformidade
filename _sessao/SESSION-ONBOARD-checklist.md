---
area: checklist
last_updated: 2026-09-23
related: [_sessao/TODO.md, _sessao/DECISOES.md, _sessao/LICOES.md, _sessao/SPEC.md, _sessao/log.md, _sessao/INFRASTRUCTURE-REFERENCE.md, BLOCKED-ON-RODRIGO.md, tests/AVALIACAO_MODELOS.md, branding/README.md, .claude/commands/onboard-checklist.md]
---

# Estado: checklist-conformidade

**O que é:** app Streamlit que transforma normativos em checklists de conformidade (Excel). O essencial é extrair os dispositivos e atribuir os responsáveis ([SPEC](SPEC.md)).

**Commits desta linha de trabalho:** `dcc3ca3` (código, branding e testes) e, em seguida, o commit de checkpoint (só documentação de sessão), ambos no `origin` (GitLab da Câmara). O remoto `github` ainda está em `3af230a` e **publica o app** quando recebe um push. Confira o estado atual com `git log --oneline -3` e `git status -sb`: não confie só neste texto.

## Onde paramos

- **Feito:**
  - provider Gemini (`gemini-3.6-flash`) ou Gemma 4 local;
  - `branding/` a partir do manual da Câmara, aplicado ao app;
  - allowlist anti-SSRF para `camara.leg.br`;
  - terminologia oficial no prompt;
  - duas rodadas exploratórias de teste de modelos, inconclusivas ([AVALIACAO_MODELOS](../tests/AVALIACAO_MODELOS.md)).
- **Problema central para pôr no ar:** o app manda o normativo inteiro numa chamada. O Gemma resume (16 de 104 itens na Portaria 227), e o Gemini gratuito devolve 503. **É preciso dividir em lotes.**
- **O app publicado hoje** (Streamlit Cloud) roda o código antigo, com a chave Gemini antiga que caiu, então não funciona.

## Próximo passo

**P0, etapa 1 do [TODO](TODO.md):** implementar no app a divisão em lotes de ~800 tokens, com progresso, nova tentativa por lote e erros reais. Parta de `dividir_em_lotes()` em `tests/eval_modelos.py`. Não depende de nenhuma decisão. Depois, etapa 2: testar localmente com a Portaria 227.

## Decisões em aberto (detalhes em [DECISOES](DECISOES.md#em-aberto-só-o-rodrigo-decide))

- **Hospedagem agora:** Streamlit Cloud com Gemini ou servidor interno com Gemma. Bloqueia as etapas 3 e 4 do P0.
- **Faturamento do Gemini:** bloqueia o uso real do Gemini.
- Revisão e conformidade do `branding/` (Comid; grafia das unidades).

## Ações que dependem do Rodrigo

Ver [BLOCKED-ON-RODRIGO.md](../BLOCKED-ON-RODRIGO.md). Em destaque: os *secrets* do Streamlit Cloud antes de qualquer push para o `github`.

## Ponteiros

- Tarefas: [TODO](TODO.md) · Decisões: [DECISOES](DECISOES.md) · Pegadinhas de ambiente: [LICOES](LICOES.md) · Linha do tempo: [log](log.md)
- Endereços, variáveis e receitas: [INFRASTRUCTURE-REFERENCE](INFRASTRUCTURE-REFERENCE.md)
- Código: `app.py` (UI) · `lib/llm.py` (providers) · `lib/extractor.py` · `lib/prompt_templates.py` · `branding/streamlit_cd/cd_brand.py`
- Testes: `tests/eval_modelos.py`, `tests/fixtures/`, `tests/resultados/`
- Metodologia completa do v1.08, a incorporar: `gerador-checklists/`, `TODO-sync-gerador-nuati.md`
- Snapshot na memória: `~/.claude/projects/C--Users-P-8106-Documents-solucoes-checklist-conformidade/memory/checklist_state_2026-09-23.md`
