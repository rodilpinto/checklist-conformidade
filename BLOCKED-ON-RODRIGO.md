# Ações que só o Rodrigo pode fazer

<!-- lista acumulativa entre sessões · 🔴 bloqueia o P0 · 🟡 importante · 🟢 quando der · detalhes nos arquivos citados -->

## Abertas

- 🟡 **Não padronizar os *secrets* do app principal até a produção receber o framework** (numa rodada futura, depois da v0.1.0). Eles têm uma exceção desde o incidente de 28/09 (valor da chave `_2` em `GEMINI_API_KEY`, mais `GEMINI_MODEL`). *Por quê:* o código no ar lê só essas variáveis. *Desbloqueia:* nada; evita quebrar produção. Ver `_sessao/DECISOES.md` (28/09 e 30/09).
- 🟢 **Acrescentar `GEMINI_MODEL = "gemini-3.5-flash-lite"` aos *secrets* dos outros apps** (bloco padrão). *Por quê:* apps com código antigo que leem `GEMINI_MODEL` voltam ao `gemini-3.6-flash` sem ela. *Desbloqueia:* *secrets* realmente uniformes. Ver `_sessao/DECISOES.md` (28/09).
- 🟡 **App público com chave gratuita:** decidir entre colocar o aviso "não envie documentos internos" ou voltar a deixá-lo privado. *Desbloqueia:* uso seguro do MVP. Ver `_sessao/DECISOES.md`.
- ℹ Push para o servidor interno (Gitea): às vezes funciona sem login (credencial em cache); se der "Authentication failed", rode `! GCM_INTERACTIVE=always git push origin <branch>` e autorize no navegador.
- 🟡 **Decidir se habilita o faturamento no projeto Google da unidade** (aistudio.google.com → projeto → "Set up billing"). *Por quê:* envolve custo e talvez as áreas de contratação e TI. *Desbloqueia:* o Gemini em produção (cota de 20 requisições/dia/modelo e uso dos dados no nível gratuito) e a comparação com o Gemini nos testes. Detalhes em `_sessao/DECISOES.md`. ⚠ Hoje está desligado nos dois projetos (conferido em 29/09); ligar reabre a D-C26.
- 🟡 **Levantar o padrão de deploy das outras soluções na rede da Câmara.** *Desbloqueia:* a hospedagem interna com o Gemma.
- 🟢 **Rotacionar a chave Gemini** (possível exposição registrada em `_sessao/INTERNO.md`). Atualizar o `.env` e os *secrets* depois.
- 🟢 **Revisar `branding/README.md`**, principalmente as adaptações digitais marcadas com 📝. Confirmar a grafia e a hierarquia das unidades na assinatura do rodapé e, se necessário, consultar a Comid (publicidade@camara.leg.br) sobre o uso da marca em ferramentas internas.
- 🟢 **Decidir o destino de 3 arquivos não rastreados na raiz**, que já existiam antes da sessão de 22/09/2026 e nunca foram commitados:
  - `MCGR-Modelo-Corporativo-Gestao-Riscos-CD.md` e `Modelo Corporativo de Gestão de Riscos da Câmara dos Deputados.pdf`: parecem a fonte da metodologia MCGR citada no commit `3af230a`. Commitar, mover para `gerador-checklists/` ou descartar. ⚠ São a fonte da metodologia MCGR usada na v1.08, que é a referência do próximo trabalho (planilha v1.08/v1.09): descartar perde essa fonte.
  - `.claude/settings.local.json`: configuração local do Claude Code. Sugestão: incluir no `.gitignore`.
  *Desbloqueia:* uma árvore de trabalho limpa.
- 🟢 (opcional) **`ANTHROPIC_API_KEY` no `.env`**, para testar o Claude pelo pipeline do app.

## Feitas

- ✅ 2026-10-01: validou o tempo economizado no ar; autorizou o passo 8; apagou o app `-v2`; trocou a branch padrão do Gitea interno para `main`.
- ✅ 2026-09-30: passo 6 do passe por app (produção recriada na `main`, app de homologação criado).
- ✅ 2026-09-29: decidiu D-C25 (o `Nuati-SECIN/framework` vira espelho interno) e D-C26 (apps públicos, faturamento desligado nos dois projetos Google), no ledger compartilhado do buscador.
- ✅ 2026-09-28: criou o app de teste (https://checklist-conformidade-v2.streamlit.app/, branch `feat/llm-cadeia`); colou os logs da nuvem; corrigiu os *secrets* do app principal depois do incidente (92 itens com a Portaria 227 inteira); criou o repositório `Nuati-SECIN/framework` no servidor interno.
- ✅ 2026-09-25: *secrets* do Streamlit Cloud com `GEMINI_MODEL = "gemini-3.5-flash-lite"` e a chave gratuita do Rodrigo; reboot; **MVP funcionando**. Hospedagem decidida: Streamlit Cloud até o servidor interno ficar pronto.

- ✅ 2026-09-23: autenticou no GitLab da Câmara pelo navegador, e o push de `dcc3ca3` para o `origin` funcionou.
- ✅ 2026-09-22: chave Gemini completa colocada no `.env`.
