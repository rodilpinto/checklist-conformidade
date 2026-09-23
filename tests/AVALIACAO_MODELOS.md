# Avaliação de modelos para o gerador de checklists

Registro do método, dos resultados e das limitações dos testes feitos em 22 e 23/09/2026 para decidir se o **Gemma 4 local** (`google/gemma-4` no servidor interno; endereço em `_sessao/INTERNO.md`) pode substituir o Gemini no app sem prejuízo.

> **Status: exploratório, inconclusivo.** Cada configuração rodou **uma única vez**. Os números servem para orientar os próximos testes, não para decidir. Ver "Limitações" antes de citar qualquer resultado.

O método foi pensado para virar um framework reutilizável na escolha de modelos de outras aplicações (seção final).

---

## 1. Objetivo e prioridades

Definidas pelo Rodrigo em 23/09/2026:

1. **Essencial:** extrair os dispositivos (artigo, parágrafo, inciso, alínea) com o texto literal e atribuir os **responsáveis** corretamente.
2. **Secundário:** a nota de risco (Impacto × Probabilidade, MCGR). É só uma referência, porque será validada por um humano de qualquer forma.

## 2. Insumos

| Insumo | Arquivo | Proveniência |
|---|---|---|
| Normativo de teste | `tests/fixtures/portaria_227_2025.txt` | ✅ Texto oficial da Portaria nº 227, de 23/12/2025 (DG), baixado de www2.camara.leg.br em 22/09/2026 (URL na 1ª linha do arquivo). São 39 artigos, 22.267 caracteres e 5.384 tokens no Gemma. |
| Referência | `gerador-checklists/checklists/Checklist_Portaria_227_2025_IA_v1.08.xlsx`, aba "Checklist Conformidade", 104 itens | ⚠ Gerado no commit `edd8923` (09/03/2026), com coautoria do Claude Opus 4.6. O texto literal confere com o oficial em 99% (os 2 casos restantes são abreviação intencional "[...]" e um artefato de HTML). Os **scores de risco e os responsáveis não tiveram revisão humana** (confirmado pelo Rodrigo em 23/09/2026). |
| Prompt | `lib/prompt_templates.py` (`build_prompt("")`, 1.677 tokens) | O mesmo prompt do app. Em 22/09/2026 ganhou a regra de usar os nomes de cargos do normativo e não usar "DPO". |

**Consequência:** cobertura e fidelidade literal são medidas contra o texto oficial, portanto confiáveis. **Responsáveis e risco são medidos contra outra geração de IA**, então indicam **concordância**, não **acerto**.

## 3. Métricas (`tests/eval_modelos.py`)

| Métrica | Definição | Observações |
|---|---|---|
| Cobertura | % dos 104 itens da referência que têm um item do modelo com texto literal semelhante (similaridade ≥ 0,85, ou um texto contido no outro com pelo menos 30 caracteres) | Omitir dispositivos declaratórios é permitido pelo prompt e conta como "não coberto" |
| Itens sem par | Itens do modelo sem correspondência na referência | Mistura granularidade mais fina com itens extras |
| Fidelidade literal | % dos itens do modelo cujo `texto_literal` normalizado aparece exatamente no texto oficial | A normalização ignora acentos, maiúsculas, espaços e o artefato de espaço antes de pontuação vindo do HTML do portal |
| Granularidade | % dos artigos em que o modelo gera o mesmo número de itens que a referência | |
| Responsáveis: condicional | Sobre os itens **cobertos**: % com pelo menos um ator da Portaria em comum com a referência | ⚠ **Enviesada quando a cobertura é baixa** (ver seção 6) |
| **Responsáveis: efetiva** | Sobre **todos** os itens da referência que têm ator: % cobertos **e** com ator em comum | Métrica principal de responsáveis a partir de 23/09/2026 |
| Papel fora da Portaria | % dos itens do modelo cujo responsável não menciona nenhum ator da Portaria | Dicionário `ATORES`: Ditec, CETIA, CGE, CGSIC, CDTI, Gestor de Negócio, Gestor de Dados, Encarregado, Gerente de Projeto, Usuário, Unidade Administrativa, Diretor-Geral (siglas e nomes por extenso) |
| Terminologia | Ocorrências de "DPO" e de "Encarregado de Proteção de Dados Pessoais" | Forma oficial decidida em 22/09/2026 |
| Risco | Concordância de Impacto e Probabilidade (exata e ±1) e do nível | Secundária |
| Tempo | Total e **maior bloco** comparados com o timeout do app (300 s) | Só para chamadas feitas pelo app |

Calibração: a referência avaliada contra ela mesma dá 100% de cobertura, 100% nos responsáveis e 100% de granularidade.

## 4. Configurações testadas

- **Divisão do texto:**
  - documento inteiro;
  - por capítulo (10 blocos);
  - por lotes de artigos consecutivos até ~N tokens de entrada (800 dá 9 lotes; 1.500 dá 4; 3.000 dá 2), cada lote com o capítulo corrente como contexto.
- **Gemma 4:** com raciocínio (padrão) e sem raciocínio (`chat_template_kwargs: {enable_thinking: false}`, ativado por `LOCAL_LLM_DISABLE_THINKING=1`).
- **Claude Opus, Sonnet e Haiku:** subagentes do Claude Code atuando como "o LLM do app". Receberam o mesmo prompt de sistema e os mesmos 4 lotes de 1.500 tokens, numa pasta isolada sem acesso à referência, e gravaram o JSON à mão. ⚠ Não passaram pelo `lib/llm.py` e não tiveram tempo medido.
- **Gemini 3.6 Flash:** tentado com o documento inteiro e por capítulo. **Sem resultado:** a chave é do nível gratuito (20 requisições/dia/modelo) e deu 503 "high demand" nas requisições grandes, depois 429.

## 5. Resultados (1 execução por configuração)

### Rodada 1 (22/09/2026): estratégias de divisão

| Configuração | Itens | Cobertura | Literal | Nível exato | Tempo | Maior bloco |
|---|---|---|---|---|---|---|
| Gemma com raciocínio, documento inteiro | 16 | 15,4% | 100% | 31% | 5 min | 299 s |
| Gemma com raciocínio, por capítulo | 102 | 96,2% | 100% | 39% | 32 min | 343 s |
| Gemma sem raciocínio, por capítulo | 116 | 98,1% | 100% | 32% | 16 min | 316 s |
| Gemini 3.6 Flash, inteiro e por capítulo | 0 | - | - | - | - | 503/429 |

Diagnóstico do documento inteiro: `finish_reason=stop` com 15.112 de 20.480 tokens. **Não houve estouro de contexto.** O Gemma resumiu por conta própria ("focus on the most critical ones... fits within output limits").

### Rodada 2 (23/09/2026): lotes de artigos e comparação com Claude

| Configuração | Itens | Cobertura | Literal | Resp. condicional | **Resp. efetiva** | Papel fora da Portaria | Nível exato | Tempo | Maior bloco | Erros |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemma sem raciocínio, lotes de 800 | 129 | 99,0% | 99,2% | 64,1% | **63,5%** | 31% | 32% | 18 min | 177 s | 0 |
| Gemma sem raciocínio, lotes de 1.500 | 74 | 64,4% | 98,6% | 89,6% | **57,7%** | 1% | 31% | 15 min | 282 s | 1 lote com JSON inválido |
| Gemma sem raciocínio, lotes de 3.000 | 94 | 81,7% | 100% | 95,3% | **77,9%** | 5% | 25% | 13 min | 514 s | 0 |
| Gemma com raciocínio, lotes de 800 | 128 | 97,1% | 99,2% | 71,3% | **69,2%** | 20% | 36% | 42 min | 490 s | 0 |
| Gemma com raciocínio, lotes de 1.500 | 105 | 98,1% | 99,0% | 70,6% | **69,2%** | 5% | - | 23 min | 401 s | 0 |
| Gemma com raciocínio, por capítulo | 102 | 96,2% | 100% | 65,0% | **62,5%** | 26% | 39% | 32 min | 343 s | 0 |
| Gemma sem raciocínio, por capítulo | 116 | 98,1% | 100% | 62,7% | **61,5%** | 27% | 32% | 16 min | 316 s | 0 |
| Opus, lotes de 1.500 (subagente) | 117 | 98,1% | 100% | 94,1% | **92,3%** | 5% | 47% | - | - | 0 |
| Sonnet, lotes de 1.500 (subagente) | 95 | 89,4%* | 100% | 73,1% | **65,4%** | 16% | 63% | - | - | 0 |
| Haiku, lotes de 1.500 (subagente) | 126 | 98,1% | 100% | 74,5% | **73,1%** | 10% | 45% | - | - | 0 |

\* O Sonnet omitiu de propósito os dispositivos declaratórios (parágrafo único do Art. 5º e seus incisos, Art. 28, definições do Art. 2º), o que o prompt permite.

Resultados brutos (itens JSON e `resumo.json` de cada execução): `tests/resultados/<timestamp>[_modelo]/`.

### Observações qualitativas

- **Papéis inventados pelo Gemma:**
  - "Gestor do sistema de IA", 13 itens (com raciocínio, por capítulo);
  - "Câmara dos Deputados", 21 itens (sem raciocínio, por capítulo).
- **Nome errado da Ditec:** o Sonnet (12 itens) e o Haiku a chamaram de "Diretoria de Tecnologia da Informação". O nome oficial é "Diretoria de Inovação e Tecnologia da Informação".
- **"DPO":** o Haiku usou "DPO" 2 vezes. Os demais, nenhuma.
- **Nível de risco:** todos os modelos divergem da referência, e o Gemma concentra em "Alto". Como a referência não foi revisada, isso não indica erro.

## 6. Leituras provisórias e correções

1. **Extração de dispositivos:** com divisão por capítulo ou por lote, todos os modelos ficam entre 96 e 99% de cobertura (exceto quando lotes são perdidos ou o modelo resume), com cerca de 100% de fidelidade literal. 📝 Não há diferença relevante entre os modelos aqui.
2. **Responsáveis:** é onde os modelos se diferenciam. Opus 92%; Gemma de 58% a 78% conforme a configuração; Haiku 73%; Sonnet 65% (resp. efetiva).
3. **Documento inteiro não serve para o Gemma.** Ele resume por conta própria.
4. **O raciocínio do Gemma** deixa tudo 2 a 2,5 vezes mais lento e estoura o timeout de 300 s. Nas duas comparações com lote de mesmo tamanho, ganha cerca de 6 pontos na resp. efetiva.
5. ⚠ **Correção de 23/09/2026:** a leitura inicial de que lotes maiores melhoram os responsáveis vinha da métrica **condicional**. Com cobertura de 64% e 82%, ela é calculada sobre um subconjunto menor e provavelmente mais fácil. Com a métrica efetiva, os lotes de 1.500 sem raciocínio são a **pior** configuração (57,7%). Os de 3.000 continuam altos (77,9%), mas numa execução só, com 82% de cobertura e maior bloco de 514 s. **Não há evidência suficiente de que o tamanho do lote melhora os responsáveis.** (Discordância levantada pelo Rodrigo.)
6. **Candidata operacional**, 📝 ainda não confirmada: Gemma sem raciocínio, lotes de ~800 tokens. É a única configuração do Gemma com cobertura ≥ 99% e todos os blocos abaixo de 300 s. O ponto fraco são os responsáveis (63,5%).

## 7. Limitações

- **Uma execução por configuração.** Sem medida de variância, diferenças abaixo de cerca de 10 pontos podem ser ruído.
- **Um único normativo**, e ainda com lista de atores bem definida. Não há garantia de generalizar.
- **A referência de responsáveis e risco é gerada por IA** (Opus 4.6), sem revisão humana. Há viés possível a favor do Opus na métrica de responsáveis, por ser da mesma família do modelo que gerou a referência.
- **Subagentes Claude ≠ pipeline do app:** gravaram o JSON pela ferramenta Write, sem tempo medido, e podem ter usado scripts auxiliares para validar o JSON (o Opus e o Sonnet usaram Node).
- **O dicionário de atores** é específico da Portaria 227 e foi ajustado durante a análise: a correção de "Comitê de Gestão Estratégica" e de "Comitê de Ética no Uso da IA" alterou números.
- **O casamento por similaridade de texto** pode parear errado dispositivos curtos e parecidos.
- **Gemini sem dados:** a comparação com o modelo que o app usava originalmente ficou pendente.

## 8. Próximos testes sugeridos

1. **Repetir cada configuração candidata 3 a 5 vezes** e reportar média e desvio.
2. **Ajuste de responsáveis no prompt:** enviar em cada lote a lista de atores do normativo (ex.: Art. 28 e Capítulo X) e exigir o nome oficial. Medir a resp. efetiva na candidata (Gemma sem raciocínio, lotes de 800).
3. **Isolar o efeito do tamanho de lote sobre os responsáveis**, com o mesmo conjunto de itens cobertos (ou com a métrica efetiva) e várias execuções. Refazer os lotes de 1.500 e 3.000 com nova tentativa em caso de JSON inválido.
4. **Validação humana às cegas:** amostra de 20 a 30 dispositivos, com responsáveis e nota avaliados pelo Rodrigo sem saber a origem (Gemma, Opus ou v1.08). Isso vira a referência de verdade para responsáveis.
5. **Segundo normativo**, o Roteiro de Levantamento SECIN 2018, que tem checklist v1.00, para testar a generalização e evitar calibrar o prompt na mesma prova.
6. **Gemini em nível pago**, pelo pipeline do app, se o faturamento for habilitado.
7. **Claude pela API**, pelo pipeline do app, com tempo e custo medidos (exige `ANTHROPIC_API_KEY`).
8. **Paralelismo no servidor local:** verificar se o llama.cpp aceita vários slots (`-np`) para processar lotes em paralelo e reduzir os 18 min.
9. **Métricas novas a considerar:** responsáveis ponderados por ator (Jaccard), itens extras classificados (granularidade mais fina ou inventado), custo por checklist.

## 9. Como reproduzir

```bash
# modelos chamados pelo app (Gemma local / Gemini)
py tests/eval_modelos.py --modelos gemma-norazao --runs 3 --modo lote --lote-tokens 800
py tests/eval_modelos.py --modelos gemma --modo capitulo
# lotes para modelos externos (subagentes) e importação do resultado
py tests/eval_modelos.py --exportar-lotes <pasta> --lote-tokens 1500
py tests/eval_modelos.py --importar <pasta> --nome opus --lote-tokens 1500
# recalcular métricas de uma execução já feita
py tests/eval_modelos.py --reavaliar tests/resultados/<pasta>
```

Pré-requisitos: `.env` com `LOCAL_LLM_URL`, `LOCAL_LLM_MODEL` e, para o Gemini, `GEMINI_API_KEY`; máquina na rede da Câmara para o Gemma.

## 10. Rumo a um framework de escolha de modelos

O que já é genérico e pode ser extraído para uso em outras aplicações:

- **Protocolo:** fixture oficial, referência com proveniência declarada, mesmas entradas e mesmo prompt para todos os modelos, várias execuções e relatório com limitações.
- **Métricas reutilizáveis:** cobertura por similaridade de texto, fidelidade literal contra a fonte, tempo por bloco contra o timeout do app, termos proibidos e obrigatórios.
- **Import e export de lotes:** permite comparar modelos fora do pipeline (subagentes, outras ferramentas) com as mesmas métricas.

O que é específico de cada aplicação e precisaria de configuração:

- Os campos do JSON e o mapeamento da referência (colunas).
- O dicionário de atores e termos.
- Os critérios de aceite. Por exemplo, "cobertura ≥ 97%, resp. efetiva ≥ 85%, todos os blocos < 300 s, 0 'DPO'".

📝 Sugestão: definir os critérios de aceite **antes** da próxima rodada, para que a escolha do modelo não dependa de leitura a posteriori dos números.
