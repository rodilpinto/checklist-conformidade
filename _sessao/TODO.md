# TODO — checklist-conformidade

<!-- last_audit: 2026-09-25 · itens concretos, mais urgentes no topo · ações que só o Rodrigo pode fazer: BLOCKED-ON-RODRIGO.md (raiz) -->

## P0: módulo comum de provedores e chaves de LLM (a partir de 25/09/2026)

- [ ] **(sessão do buscador-normativos)** Criar o módulo comum de LLM para todos os MVPs:
  - sequência LLM local → chave NUATI → chave Rodrigo → chave digitada pelo usuário (📝 sugestão: a do usuário primeiro, quando informada);
  - vários modelos por chave;
  - pular para a próxima opção em 429, 503, 404 e 400;
  - `thinking_budget` só para os modelos que aceitam;
  - mostrar qual opção atendeu;
  - avaliar Groq, Cerebras e OpenRouter (gratuitos) e Anthropic (chave paga com créditos).
  Depois, **trazer para cá**, integrando em `lib/llm.py` (`generate_checklist` / `_call_gemini`) e em `app.py` (`_render_sidebar`). Os fatos úteis estão em `LICOES.md`.
- [ ] Depois do módulo: retomar `pausado-2026-09-25-lotes-e-erros.patch` (divisão em lotes e mensagens de erro reais) com teste local da Portaria 227 antes de publicar. Sem os lotes, normativos grandes dependem de o `gemini-3.5-flash-lite` dar conta numa chamada só (deu conta da Portaria 227 em 75 s).
- [ ] 📝 App público: aviso na tela "não envie documentos internos ou com dados pessoais" (plano gratuito), ou voltar a deixá-lo privado. Decisão do Rodrigo.
- [x] (25/09) Commits enviados ao GitLab interno (`059591a`).

## P1: logo depois

- [ ] 📝 Candidato a funcionalidade da **v2.0** do app (ideia do Rodrigo, 23/09/2026): trazer para o app o que hoje só existe nos geradores de `gerador-checklists/`. O item abaixo é o ponto de partida.
- [ ] Incorporar no app os elementos do v1.08 que o app não tem:
  - colunas "Princípio / Tema" e "Precedência (decorrências)";
  - aba "Ações – Todos os Atores" (ator, fase, ação, artigo, texto literal, entregável, interação com);
  - "Resumo por Capítulo" e "Legenda e Instruções".
  - O v1.08 foi aprimorado por uma skill nunca incorporada ao app. Ver também `TODO-sync-gerador-nuati.md` e os scripts em `gerador-checklists/scripts/create_v108.py`.
- [ ] 📝 Prompt: instruir o modelo a usar como responsáveis só os papéis nomeados no normativo, com o nome oficial. O Gemma inventou "Gestor do sistema de IA"; o Sonnet e o Haiku erraram o nome da Ditec.

## P2: testes de modelo (pausados; roteiro em `tests/AVALIACAO_MODELOS.md`, seção 8)

- [ ] Definir os critérios de aceite **antes** da próxima rodada.
- [ ] Repetir as configurações candidatas de 3 a 5 vezes; testar o prompt com a lista de atores; fazer a validação humana às cegas de 20 a 30 itens; testar num segundo normativo (Roteiro SECIN 2018).
- [ ] Gemini em nível pago e Claude pela API, pelo pipeline do app (dependem de faturamento ou chave).

## P3: branding e outros apps

- [ ] (Rodrigo) Revisar `branding/README.md` (itens 📝).
- [ ] Aplicar `branding/` nos outros apps: DOU-clipping-app, pesquisa_diario, scopediagram, wiki-chat (HTML via `tokens.css`), auditflowmongodb (hoje com `nuati.css` próprio).
- [ ] Sincronizar com a metodologia completa de `gerador-checklists/` (`TODO-sync-gerador-nuati.md`).

## Feito

- [x] 2026-09-25: **MVP no ar funcionando** (confirmado pelo Rodrigo): `69f8c53` permite modelos "lite"; *secrets* com `GEMINI_MODEL = "gemini-3.5-flash-lite"` e a chave do Rodrigo; snapshot `090aa67` publicado no GitHub.

- [x] 2026-09-23: rodada 2 de testes (lotes de artigos × Gemma com e sem raciocínio × subagentes Opus, Sonnet e Haiku), registrada em `tests/AVALIACAO_MODELOS.md`. Commit `dcc3ca3`.
- [x] 2026-09-23: pesquisa do que é preciso para o Gemini funcionar (`DECISOES.md`).
- [x] 2026-09-23: dados internos movidos para `_sessao/INTERNO.md`; primeiro snapshot público publicado no GitHub via `scripts/publicar_github.sh` (sem `INTERNO.md`; o `gerador-checklists/` foi incluído num segundo snapshot, a pedido do Rodrigo). O Streamlit Cloud republicou; faltam os *secrets*.
- [x] 2026-09-23: commit `dcc3ca3` enviado ao `origin` (GitLab interno).
- [x] 2026-09-22: rodada 1 de testes (documento inteiro × por capítulo).
- [x] 2026-09-22: chave Gemini nova no `.env`, testada com o gemini-3.6-flash.
- [x] 2026-09-22: guia de identidade visual (`branding/`) criado e aplicado ao app (validado por screenshot local).
- [x] 2026-09-22: provider LLM local, allowlist anti-SSRF, terminologia oficial no prompt, README com a URL de deploy.
