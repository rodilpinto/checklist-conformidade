# Ações que só o Rodrigo pode fazer

<!-- lista acumulativa entre sessões · 🔴 bloqueia o P0 · 🟡 importante · 🟢 quando der · detalhes nos arquivos citados -->

## Abertas

- 🟡 **Levar o relatório do servidor do Nuati à sessão do framework** (`_sessao/relatorio-servidor-nuati-para-framework.md`; basta pedir que ela leia o arquivo com `git -C ../checklist-conformidade show origin/homologacao:_sessao/relatorio-servidor-nuati-para-framework.md`). *Desbloqueia:* o recurso de implantação no framework e o prompt para o passe do buscador no servidor.
- 🟡 **Não padronizar os *secrets* do app principal até a produção receber o framework** (numa rodada futura; a v0.1.0 foi aprovada em 01/10, então essa rodada já pode acontecer, com o seu ok: item 3 do próximo passo no `_sessao/SESSION-ONBOARD-checklist.md`). Eles têm uma exceção desde o incidente de 28/09 (valor da chave `_2` em `GEMINI_API_KEY`, mais `GEMINI_MODEL`). *Por quê:* o código no ar lê só essas variáveis. *Desbloqueia:* nada; evita quebrar produção. Ver `_sessao/DECISOES.md` (28/09 e 30/09).
- 🟢 **Acrescentar `GEMINI_MODEL = "gemini-3.5-flash-lite"` aos *secrets* dos outros apps** (bloco padrão). *Por quê:* apps com código antigo que leem `GEMINI_MODEL` voltam ao `gemini-3.6-flash` sem ela. *Desbloqueia:* *secrets* realmente uniformes. Ver `_sessao/DECISOES.md` (28/09).
- 🟡 **App público com chave gratuita:** decidir entre colocar o aviso "não envie documentos internos" ou voltar a deixá-lo privado. *Desbloqueia:* uso seguro do MVP. Ver `_sessao/DECISOES.md`.
- ℹ Push para o servidor interno (Gitea): às vezes funciona sem login (credencial em cache); se der "Authentication failed", rode `! GCM_INTERACTIVE=always git push origin <branch>` e autorize no navegador.
- 🟡 **Decidir se habilita o faturamento no projeto Google da unidade** (aistudio.google.com → projeto → "Set up billing"). *Por quê:* envolve custo e talvez as áreas de contratação e TI. *Desbloqueia:* o Gemini em produção (cota de 20 requisições/dia/modelo e uso dos dados no nível gratuito) e a comparação com o Gemini nos testes. Detalhes em `_sessao/DECISOES.md`. ⚠ Hoje está desligado nos dois projetos (conferido em 29/09); ligar reabre a D-C26.
- 🟢 **Rotacionar a chave Gemini** (possível exposição registrada em `_sessao/INTERNO.md`). Atualizar o `.env` e os *secrets* depois.
- 🟢 **Revisar `branding/README.md`**, principalmente as adaptações digitais marcadas com 📝. Confirmar a grafia e a hierarquia das unidades na assinatura do rodapé e, se necessário, consultar a Comid (publicidade@camara.leg.br) sobre o uso da marca em ferramentas internas.
- 🟢 **`.claude/settings.local.json` não rastreado na raiz** (configuração local do Claude Code). Sugestão: incluir no `.gitignore`. *Desbloqueia:* uma árvore de trabalho limpa.
- 🟢 (opcional) **`ANTHROPIC_API_KEY` no `.env`**, para testar o Claude pelo pipeline do app.

## Feitas

- ✅ 2026-10-01: disse que o MCGR é documento público; os 2 arquivos foram versionados em `referencias/` (o PDF renomeado para `MCGR-Modelo-Corporativo-Gestao-Riscos-CD.pdf`).
- ✅ 2026-10-01: padrão de deploy na rede resolvido na prática: tarefa agendada do Windows, no modelo do AppDOU (`servidor/`), com o app no servidor do Nuati e o LLM local alcançável de lá.
- ✅ 2026-10-01: instalou o app no servidor do Nuati (`servidor/instalar_tarefa.ps1`, porta 8401; detalhes em `_sessao/INTERNO.md`).
- ✅ 2026-10-01: validou o tempo economizado no ar; autorizou o passo 8; apagou o app `-v2`; trocou a branch padrão do Gitea interno para `main`.
- ✅ 2026-09-30: passo 6 do passe por app (produção recriada na `main`, app de homologação criado).
- ✅ 2026-09-29: decidiu D-C25 (o `Nuati-SECIN/framework` vira espelho interno) e D-C26 (apps públicos, faturamento desligado nos dois projetos Google), no ledger compartilhado do buscador.
- ✅ 2026-09-28: criou o app de teste (https://checklist-conformidade-v2.streamlit.app/, branch `feat/llm-cadeia`); colou os logs da nuvem; corrigiu os *secrets* do app principal depois do incidente (92 itens com a Portaria 227 inteira); criou o repositório `Nuati-SECIN/framework` no servidor interno.
- ✅ 2026-09-25: *secrets* do Streamlit Cloud com `GEMINI_MODEL = "gemini-3.5-flash-lite"` e a chave gratuita do Rodrigo; reboot; **MVP funcionando**. Hospedagem decidida: Streamlit Cloud até o servidor interno ficar pronto.

- ✅ 2026-09-23: autenticou no GitLab da Câmara pelo navegador, e o push de `dcc3ca3` para o `origin` funcionou.
- ✅ 2026-09-22: chave Gemini completa colocada no `.env`.
