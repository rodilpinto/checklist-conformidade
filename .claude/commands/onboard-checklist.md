---
description: Retomar o trabalho no checklist-conformidade a partir dos arquivos de estado
---

Você está retomando o trabalho no app **checklist-conformidade**. Leia, nesta ordem:

1. `_sessao/SESSION-ONBOARD-checklist.md`: estado atual e próximo passo (porta de entrada).
2. `_sessao/TODO.md`: tarefas por prioridade.
3. `_sessao/DECISOES.md`: decisões tomadas e, principalmente, "Em aberto" (só o Rodrigo decide).
4. Decisões compartilhadas, sempre na versão do servidor (os checkouts locais podem estar atrás):
   - entre os apps (ambientes, apps públicos): `git -C ../buscador-normativos fetch -q origin` e `git -C ../buscador-normativos show origin/master:_DECISOES-PENDENTES.md` (D-C mais recentes);
   - do framework: `git -C ../nuati-framework fetch -q origin` e `git -C ../nuati-framework show origin/homologacao:DECISOES.md` (seção "Abertas").
5. `BLOCKED-ON-RODRIGO.md`: ações que só o Rodrigo pode fazer.
6. `_sessao/LICOES.md`: pegadinhas de ambiente e de processo.
7. `_sessao/INFRASTRUCTURE-REFERENCE.md`: endereços, variáveis e receitas. Os valores internos da rede da Câmara (IP do LLM, servidor git interno, conta Google) ficam em `_sessao/INTERNO.md`, versionado só no servidor interno (o `publicar_snapshot` o exclui dos snapshots do GitHub público).
8. Leitura rápida: `_sessao/log.md` (entrada mais recente) e `_sessao/SPEC.md`.
9. Se o trabalho envolver o framework: `git -C ../nuati-framework show origin/homologacao:README.md` (§2 regra de sincronia, §3 ambientes e dia a dia, §4 registro de cópias) e o README de cada pasta de recurso no próprio app.
10. Se for mexer na planilha de saída (`lib/excel_builder.py`): a referência é `gerador-checklists/checklists/Checklist_Portaria_227_2025_IA_v1.08.xlsx`, o script `gerador-checklists/scripts/create_v108.py` e `TODO-sync-gerador-nuati.md`.
11. Se for mexer em modelos ou na avaliação: `tests/AVALIACAO_MODELOS.md`.
12. Se o estado parecer incompleto: o snapshot mais recente em `~/.claude/projects/C--Users-P-8106-Documents-solucoes-checklist-conformidade/memory/` (índice em `MEMORY.md`).

Rode `git log --oneline -3` e `git status -sb` para comparar o estado real com o registrado. Testes: `py -m pytest -q` (da raiz). O `github` recebe snapshots com histórico próprio (não é ancestral das branches locais); para ver o que cada app publica, rode `git ls-remote github`.

Depois, mostre ao usuário um resumo de até 8 linhas: estado atual, último commit, próximo passo e decisões em aberto.

Se a mensagem do usuário já trouxe uma tarefa, siga com ela depois do resumo. Se não trouxe, pergunte "Qual a tarefa de hoje?" e PARE. Não invente trabalho.

Regras do projeto:
- registrar decisões, lições, tarefas e escopo em `_sessao/` (convenção project-journal);
- separar ✅ documentado de 📝 sugestão;
- **nunca** `git push github` direto: o GitHub é público e publica os apps. Use `bash publicar_snapshot/publicar_snapshot.sh --ramo <branch>` (com `--simular` antes; configuração em `publicar_snapshot.conf`) e confira os *secrets* do app contra as variáveis que o código daquela branch lê;
- **não editar as pastas do framework** (`llm_cadeia/`, `branding/`, `extracao_texto/`, `tempo_economizado/`, `publicar_snapshot/`): cópia não se edita; defeito vira pedido à sessão do framework;
- trabalho do dia a dia na `homologacao`; a `main` (produção) só muda com o ok do Rodrigo;
- dados internos da rede ficam só em `_sessao/INTERNO.md`.
