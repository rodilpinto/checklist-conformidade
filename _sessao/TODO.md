# TODO — checklist-conformidade

<!-- last_audit: 2026-09-23 · itens concretos, mais urgentes no topo · ações que só o Rodrigo pode fazer: BLOCKED-ON-RODRIGO.md (raiz) -->

## P0: pôr no ar uma versão funcional (prioridade desde 2026-09-23)

- [ ] **1. Dividir o normativo em lotes dentro do app.**
  - Portar para o `lib/llm.py` (ou para um novo `lib/lotes.py`) a divisão `dividir_em_lotes()` de `tests/eval_modelos.py`, com ~800 tokens de entrada por lote e o capítulo corrente como contexto.
  - Em `app.py`: barra de progresso lote a lote.
  - Nova tentativa por lote em caso de JSON inválido e de 503/429, com backoff.
  - Juntar os itens e rodar `validate_items`.
  - Trocar a mensagem genérica "verifique sua conexão" (`_handle_api_error`) pelo erro real.
  - Rever o timeout local (hoje 300 s por chamada).
  - Não depende de nenhuma decisão.
- [ ] **2. Testar localmente** a Portaria 227 (`tests/fixtures/portaria_227_2025.txt`) com o Gemma sem raciocínio e com o Gemini. Critério mínimo: nenhum lote perdido e cobertura comparável à rodada 2 (`tests/AVALIACAO_MODELOS.md`; dá para medir exportando os itens e usando `--importar`, ou com `eval_modelos.py --modo lote`).
- [ ] **3. (Rodrigo) Atualizar os *secrets* no Streamlit Cloud** antes do push para o GitHub. Ver `BLOCKED-ON-RODRIGO.md`. *Bloqueado pela decisão de hospedagem.*
- [ ] **4. Publicar:** `git push github master` (**isso publica**) e conferir o app no ar. *Bloqueado pela etapa 3 e pela decisão de hospedagem.*
- [ ] **5. Em paralelo (Rodrigo):** decidir o faturamento do Gemini e levantar o padrão de deploy interno para o Gemma (`DECISOES.md`, seção "Em aberto").

## P1: logo depois

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

- [x] 2026-09-23: rodada 2 de testes (lotes de artigos × Gemma com e sem raciocínio × subagentes Opus, Sonnet e Haiku), registrada em `tests/AVALIACAO_MODELOS.md`. Commit `dcc3ca3`.
- [x] 2026-09-23: pesquisa do que é preciso para o Gemini funcionar (`DECISOES.md`).
- [x] 2026-09-23: commit `dcc3ca3` enviado ao `origin` (GitLab da Câmara). O `github` continua em `3af230a`.
- [x] 2026-09-22: rodada 1 de testes (documento inteiro × por capítulo).
- [x] 2026-09-22: chave Gemini nova no `.env`, testada com o gemini-3.6-flash.
- [x] 2026-09-22: guia de identidade visual (`branding/`) criado e aplicado ao app (validado por screenshot local).
- [x] 2026-09-22: provider LLM local, allowlist anti-SSRF, terminologia oficial no prompt, README com a URL de deploy.
