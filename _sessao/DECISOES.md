# DECISOES — checklist-conformidade

<!-- last_updated: 2026-09-23 -->

## Tomadas

- **2026-09-22** ✅ O app suporta dois providers de LLM, escolhidos na sidebar: Google Gemini (nuvem) e LLM local OpenAI-compatible (`LOCAL_LLM_URL`, `LOCAL_LLM_MODEL`). Decidido pelo Rodrigo. Motivo: a chave do Gemini caiu, e há um servidor interno com `google/gemma-4` (endereço e origem em `INTERNO.md`).
- **2026-09-22** ✅ O deploy definitivo vai migrar do Streamlit Cloud público para dentro da rede da Câmara, porque o Streamlit Cloud não alcança o IP interno do LLM. O Rodrigo vai levantar como as outras soluções foram implantadas, para padronizar.
- **2026-09-22** ✅ Proteção anti-SSRF do extrator de URL: allowlist de domínios institucionais (`camara.leg.br` por padrão, configurável em `EXTRACTOR_TRUSTED_DOMAINS`), que podem resolver para IP privado. Os demais IPs privados e reservados continuam bloqueados.
- **2026-09-22** ✅ Terminologia de referência: **"Encarregado de Proteção de Dados Pessoais"**, a forma do texto oficial da Portaria 227/2025 (decidido pelo Rodrigo). "Encarregado de Dados Pessoais", usado no v1.08 e no `TODO-sync-gerador-nuati.md`, fica como forma não oficial. O prompt do app exige os nomes de cargos exatamente como no normativo e proíbe "DPO".
- **2026-09-22** ✅ A identidade visual de todos os apps NUATI fica em `branding/` neste repo (decidido pelo Rodrigo), com `branding/README.md` como ponto de referência. A base é o Manual de Identidade Visual oficial da Câmara (v4.00, dez/2025), escolhido pelo Rodrigo a partir do site camara.leg.br. É uma aplicação da marca da Câmara, não uma marca nova: o MIV p.22 proíbe criar marcas próprias para unidades e serviços internos.
- **2026-09-22** 📝 Adaptações digitais que propus (ainda sem revisão): verde de ação `#2F7958` e verde-escuro `#004A2F`, tirados do portal, porque o Verde CD tem só 2,85:1 de contraste; fundo secundário `#E5F7EC`, amostrado do MIV; rodapé com assinatura "Secretaria de Controle Interno / Núcleo de Auditoria de TI", sem siglas (MIV p.14).
- **2026-09-22** ✅ Chave Gemini da conta Google da unidade no `.env`, no formato novo `AQ.`. O `lib/llm.py` aceita `AIza` e `AQ.`.
- **2026-09-22 / 23** ✅ Modelo Gemini padrão: `gemini-3.6-flash`, porque o `gemini-2.5-flash` responde 404 para contas novas. Pode ser trocado por `GEMINI_MODEL`. Confirmado pelo Rodrigo em 23/09/2026.
- **2026-09-22 / 23** ✅ Avaliação de modelos: Gemma 4 comparado com o checklist v1.08 da Portaria 227/2025 (texto oficial como fonte), com o Gemini 3.6 Flash (sem resultado, por causa do nível gratuito) e com Claude Opus, Sonnet e Haiku (via subagentes, em lugar da API Anthropic). Método e resultados: `tests/AVALIACAO_MODELOS.md`.
- **2026-09-23** ✅ Os scores de risco do v1.08 **não foram revisados** por humano (Rodrigo). Não é impeditivo: a nota é só referência e será validada por um humano de qualquer forma. **O essencial é extrair os dispositivos e atribuir os responsáveis.**
- **2026-09-23** ✅ **Prioridade atual: pôr no ar uma versão funcional do app.** Os testes de modelo (inconclusivos, 1 execução por configuração) e a incorporação dos elementos do v1.08 ficam para depois.
- **2026-09-23** ✅ Push para o remoto `github` (rodilpinto) **equivale a publicar**: o Streamlit Cloud republica a partir dele. Só fazer como etapa do deploy, depois de atualizar os *secrets*.

- **2026-09-23** ✅ O GitHub `rodilpinto/checklist-conformidade` é **público**. Ele recebe só um snapshot, via `scripts/publicar_github.sh`, **sem** `_sessao/INTERNO.md` (dados de rede, conta e nomes) e **sem** `gerador-checklists/` (material de trabalho da auditoria). O histórico completo fica no GitLab interno. Decidido pelo Rodrigo.
- **2026-09-23** ✅ Publicar mesmo antes de atualizar os *secrets* do Streamlit Cloud (o app no ar já estava quebrado; decisão do Rodrigo).

## Evidência dos testes (não é decisão)

Todos os números ficam em **`tests/AVALIACAO_MODELOS.md`** (fonte única). Leituras qualitativas relevantes para decidir:
- 📝 O app atual manda o normativo inteiro numa chamada e **não funciona bem com normativos grandes**. O Gemma resume por conta própria, e o Gemini gratuito recusa com 503. É preciso dividir em lotes.
- 📝 A candidata operacional, ainda não confirmada, é o Gemma sem raciocínio, em lotes de ~800 tokens. O ponto fraco é a atribuição de responsáveis.
- ⚠ O Rodrigo discordou da leitura inicial sobre os lotes de 1.500 tokens, e tinha razão: a métrica de responsáveis era condicional à cobertura. A correção está documentada.

## Gemini: o que é preciso para funcionar (pesquisa de 2026-09-23; fontes em ai.google.dev)

- ✅ (docs de billing) Sair do nível gratuito: em aistudio.google.com, projeto → "Set up billing" → vincular uma conta de faturamento do Google Cloud (pré-pago a partir de US$ 5, ou pós-pago). **Não precisa de chave nova.** Teto de gasto no Tier 1: US$ 250.
- ✅ (docs de pricing) gemini-3.6-flash: US$ 0,75 por 1M de tokens de entrada e US$ 3,75 por 1M de saída até 31/12/2026, dobrando em 01/01/2027. 📝 Minha conta: cerca de US$ 0,10 por checklist da Portaria 227.
- ✅ (termos da API) **No nível gratuito, prompts e respostas podem ser usados pelo Google, com revisão humana, para melhorar produtos. No pago, não.** ⚠ Isso é inadequado para documentos internos. A própria Portaria 227 (Arts. 8º e 19) veda submeter dados pessoais ou restritos.
- 📝 A documentação não garante que o nível pago reduza os 503 ("high demand"). O recomendado é backoff exponencial com jitter para 429, 408 e 5xx.
- 📝 A pesquisa afirmava que chaves `AQ.` exigem google-genai ≥2.18.1, mas testei: funcionam com o 1.75.0 instalado.

## Em aberto (só o Rodrigo decide)

- **Onde hospedar a versão funcional agora.**
  - (a) Streamlit Cloud (URL atual), paliativo: só com o Gemini, sujeito à cota e ao uso dos dados do nível gratuito (ou pago, se habilitado).
  - (b) Servidor na rede da Câmara: funciona com o Gemma, sem custo e sem os dados saírem da rede, mas depende do levantamento de padrão de deploy.
  - **Bloqueia:** as etapas 3 e 4 do plano de deploy (`TODO.md`). **Não bloqueia** a etapa 1 (dividir em lotes), que vale para as duas opções.
- **Habilitar faturamento no projeto Google da unidade?** É condição para usar o Gemini em produção, tanto pela cota (20 requisições/dia/modelo) quanto pelo uso dos dados. Talvez envolva as áreas de contratação e TI. **Bloqueia:** a opção (a) acima para uso real e a comparação com o Gemini nos testes.
- 📝 Confirmar com a Comid (publicidade@camara.leg.br) se ferramentas internas precisam de autorização prévia para usar a marca (MIV p.20-21). **Bloqueia:** nada técnico; é conformidade do `branding/`.
- 📝 Confirmar a grafia e a hierarquia oficiais das unidades na assinatura do rodapé. **Bloqueia:** a versão final do `branding/`.
- Revisar as adaptações digitais do `branding/` (itens 📝 acima). **Bloqueia:** aplicar o `branding/` nos outros apps.
