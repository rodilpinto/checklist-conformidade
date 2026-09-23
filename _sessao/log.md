# log — checklist-conformidade

<!-- linha do tempo, mais recente no topo; só acrescentar -->

## 2026-09-23 | publicação no GitHub público

- Descoberto que o GitHub `rodilpinto/checklist-conformidade` é público. IP do LLM, conta Google, GitLab interno e nome de colega foram movidos para `_sessao/INTERNO.md`, com marcadores no restante.
- `scripts/publicar_github.sh` publica um snapshot sem `INTERNO.md` e sem `gerador-checklists/` (material de auditoria; decisão do Rodrigo), com trava que aborta se achar dado interno.
- Primeiro snapshot publicado; o Streamlit Cloud republicou. Depois, o Rodrigo liberou o `gerador-checklists/`, e ele foi incluído num segundo snapshot. O app só funciona depois que o Rodrigo atualizar os *secrets*.

## 2026-09-23 | testes de modelo (rodada 2), pesquisa do Gemini, commit e push, checkpoint

- Rodada 2 de testes: lotes de artigos (800, 1.500 e 3.000 tokens) × Gemma com e sem raciocínio, mais subagentes Opus, Sonnet e Haiku nos mesmos lotes, sem acesso à referência. Novas métricas: responsáveis (condicional e efetiva) e granularidade.
- O Rodrigo definiu o essencial (dispositivos e responsáveis; a nota de risco é só referência) e confirmou que os scores do v1.08 não foram revisados.
- O Rodrigo discordou da leitura sobre os lotes de 1.500; a métrica condicional estava enviesada. Corrigido e documentado em `tests/AVALIACAO_MODELOS.md`.
- Pesquisa do Gemini: faturamento, preço e uso dos dados no nível gratuito (`DECISOES.md`).
- Commit `dcc3ca3` (85 arquivos) enviado ao `origin`, com o login do Rodrigo no navegador. O `github` continua em `3af230a`.
- Nova prioridade: pôr no ar uma versão funcional. Checkpoint para abrir uma sessão nova.

## 2026-09-22 | deploy investigado, provider LLM local, branding, rodada 1 de testes

- Descoberto o app em checklist-conformidade.streamlit.app (privado; a chave Gemini antiga tinha caído).
- `lib/llm.py`: provider local OpenAI-compatible (Gemma 4 no servidor interno), `gemini-3.6-flash`, chaves `AQ.`. `lib/extractor.py`: allowlist `camara.leg.br` no anti-SSRF.
- `branding/` criado a partir do MIV v4.00 da Câmara e aplicado ao app.
- Terminologia oficial "Encarregado de Proteção de Dados Pessoais" no prompt.
- Rodada 1 de testes (documento inteiro × por capítulo): o Gemma resume o documento inteiro; o Gemini gratuito dá 503 e 429.
- `_sessao/` criado (convenção project-journal).
