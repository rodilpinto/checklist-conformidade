---
description: Retomar o trabalho no checklist-conformidade a partir dos arquivos de estado
---

Você está retomando o trabalho no app **checklist-conformidade**. Leia, nesta ordem:

1. `_sessao/SESSION-ONBOARD-checklist.md`: estado atual e próximo passo (porta de entrada).
2. `_sessao/TODO.md`: tarefas por prioridade (P0 a P3).
3. `_sessao/DECISOES.md`: decisões tomadas e, principalmente, "Em aberto" (só o Rodrigo decide).
4. `BLOCKED-ON-RODRIGO.md`: ações que só o Rodrigo pode fazer.
5. `_sessao/LICOES.md`: pegadinhas de ambiente (Python via `py`, arquivos com CRLF, push interativo, o remoto `github` publica o app).
6. `_sessao/INFRASTRUCTURE-REFERENCE.md`: endereços, variáveis e receitas. Os valores internos da rede da Câmara (IP do LLM, GitLab, conta Google) ficam em `_sessao/INTERNO.md`, que só existe no GitLab interno e nunca vai para o GitHub público.
7. Leitura rápida: `_sessao/log.md` (entrada mais recente) e `_sessao/SPEC.md`.
8. Se for mexer em modelos ou testes: `tests/AVALIACAO_MODELOS.md`.
9. Se o estado parecer incompleto: o snapshot mais recente em `~/.claude/projects/C--Users-P-8106-Documents-solucoes-checklist-conformidade/memory/` (índice em `MEMORY.md`).

Rode `git log --oneline -3` e `git status -sb` para comparar o estado real com o registrado. O `github` recebe snapshots com histórico próprio (não é ancestral do `master`); para saber o que já foi publicado, rode `bash scripts/publicar_github.sh --simular`.

Depois, mostre ao usuário um resumo de até 8 linhas: estado atual, último commit, próximo passo e decisões em aberto.

Se a mensagem do usuário já trouxe uma tarefa, siga com ela depois do resumo. Se não trouxe, pergunte "Qual a tarefa de hoje?" e PARE. Não invente trabalho.

Regras do projeto: registrar decisões, lições, tarefas e escopo em `_sessao/` (convenção project-journal); separar ✅ documentado de 📝 sugestão; **nunca** `git push github` direto: o GitHub é público e publica o app. Use `bash scripts/publicar_github.sh` depois de atualizar os *secrets*. Dados internos da rede ficam só em `_sessao/INTERNO.md`.
