# Ações que só o Rodrigo pode fazer

<!-- lista acumulativa entre sessões · 🔴 bloqueia o P0 · 🟡 importante · 🟢 quando der · detalhes nos arquivos citados -->

## Abertas

- 🔴 **Decidir onde hospedar a versão funcional agora:** Streamlit Cloud com Gemini (paliativo) ou servidor interno com Gemma. *Por quê:* só você decide. *Desbloqueia:* as etapas 3 e 4 do P0 em `_sessao/TODO.md`. Opções e trade-offs em `_sessao/DECISOES.md`, seção "Em aberto".
- 🔴 **Atualizar os *secrets* do app no Streamlit Cloud** (painel share.streamlit.io → app `checklist-conformidade` → Settings → Secrets), se a hospedagem for o Streamlit Cloud:
  ```toml
  GEMINI_API_KEY = "<chave AQ. completa da conta Google da unidade>"
  GEMINI_MODEL = "gemini-3.6-flash"
  ```
  *Por quê:* é interface web autenticada, e a chave é sua. *Desbloqueia:* o push para o `github`, que republica o app. 📝 Premissa a confirmar: secrets de nível raiz viram variáveis de ambiente lidas pelo `os.getenv` do app.
- 🟡 **Decidir se habilita o faturamento no projeto Google da unidade** (aistudio.google.com → projeto → "Set up billing"). *Por quê:* envolve custo e talvez as áreas de contratação e TI. *Desbloqueia:* o Gemini em produção (cota de 20 requisições/dia/modelo e uso dos dados no nível gratuito) e a comparação com o Gemini nos testes. Detalhes em `_sessao/DECISOES.md`.
- 🟡 **Levantar o padrão de deploy das outras soluções na rede da Câmara.** *Desbloqueia:* a hospedagem interna com o Gemma.
- 🟢 **Rotacionar a chave Gemini** (possível exposição registrada em `_sessao/INTERNO.md`). Atualizar o `.env` e os *secrets* depois.
- 🟢 **Revisar `branding/README.md`**, principalmente as adaptações digitais marcadas com 📝. Confirmar a grafia e a hierarquia das unidades na assinatura do rodapé e, se necessário, consultar a Comid (publicidade@camara.leg.br) sobre o uso da marca em ferramentas internas.
- 🟢 **Decidir o destino de 3 arquivos não rastreados na raiz**, que já existiam antes da sessão de 22/09/2026 e nunca foram commitados:
  - `MCGR-Modelo-Corporativo-Gestao-Riscos-CD.md` e `Modelo Corporativo de Gestão de Riscos da Câmara dos Deputados.pdf`: parecem a fonte da metodologia MCGR citada no commit `3af230a`. Commitar, mover para `gerador-checklists/` ou descartar.
  - `.claude/settings.local.json`: configuração local do Claude Code. Sugestão: incluir no `.gitignore`.
  *Desbloqueia:* uma árvore de trabalho limpa.
- 🟢 (opcional) **`ANTHROPIC_API_KEY` no `.env`**, para testar o Claude pelo pipeline do app.

## Feitas

- ✅ 2026-09-23: autenticou no GitLab da Câmara pelo navegador, e o push de `dcc3ca3` para o `origin` funcionou.
- ✅ 2026-09-22: chave Gemini completa colocada no `.env`.
