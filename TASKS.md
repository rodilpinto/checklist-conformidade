# Checklist de Tarefas - App Gerador de Checklist

## Trilha 1: Infraestrutura (sem dependencias)
- [ ] 1.1 Criar estrutura de diretórios (checklist-app/, lib/, .streamlit/)
- [ ] 1.2 Criar requirements.txt com todas as dependências
- [ ] 1.3 Criar .streamlit/config.toml (tema, layout)
- [ ] 1.4 Criar .env.example com GEMINI_API_KEY
- [ ] 1.5 Criar lib/__init__.py

## Trilha 2: Extração de Texto - lib/extractor.py (sem dependencias)
- [ ] 2.1 Função extract_from_pdf(file) -> str (pymupdf/fitz)
- [ ] 2.2 Função extract_from_docx(file) -> str (python-docx)
- [ ] 2.3 Função extract_from_url(url) -> str (requests + BeautifulSoup)
- [ ] 2.4 Função extract_text(source) -> str (dispatcher unificado)
- [ ] 2.5 Tratamento de erros e encoding UTF-8

## Trilha 3: LLM + Prompt - lib/llm.py e lib/prompt_templates.py (sem dependencias)
- [ ] 3.1 Criar prompt de sistema para análise normativa (prompt_templates.py)
  - Instruções para extrair artigos/incisos/parágrafos
  - Formato JSON de saída com campos: capitulo, artigo, texto_literal, requisito, risco, nivel, mitigacao, responsavel, evidencia
  - Regras: texto literal nunca parafraseado, terminologia oficial
- [ ] 3.2 Função call_gemini(text, extra_prompt, api_key) -> list[dict] (llm.py)
  - Integração com google-generativeai SDK
  - Modelo: gemini-2.0-flash
  - Parsing do JSON retornado
- [ ] 3.3 Validação do JSON retornado (schema, campos obrigatórios)
- [ ] 3.4 Tratamento de erros (rate limit, token limit, JSON malformado)

## Trilha 4: Geração Excel - lib/excel_builder.py (sem dependencias)
- [ ] 4.1 Definir estilos (header, seções, dados, riscos) baseados nos scripts existentes
- [ ] 4.2 Função build_excel(items: list[dict]) -> bytes
  - Headers: N, Capitulo, Artigo, Texto Literal, Requisito, Risco, Nivel, Mitigacao, Responsavel, Evidencia, Status, Obs
  - Cores por nível de risco (Critico=vermelho, Alto=laranja, Medio=amarelo, Baixo=verde)
  - Formatação profissional (bordas, alternância de linhas, auto-filtro, freeze panes)
  - Data validation para Status e Nivel
- [ ] 4.3 Retornar BytesIO para download direto no Streamlit

## Trilha 5: Interface Streamlit - app.py (DEPENDE de Trilhas 2, 3, 4)
- [ ] 5.1 Layout principal: título, descrição, duas colunas
- [ ] 5.2 Coluna esquerda: tabs ou radio para modo de entrada (Upload / Texto / URL)
- [ ] 5.3 Campo de upload (aceita .pdf e .docx)
- [ ] 5.4 Campo de texto (st.text_area para colar normativo)
- [ ] 5.5 Campo de URL
- [ ] 5.6 Campo de prompt extra (st.text_area)
- [ ] 5.7 Campo de API key (sidebar, com opção de .env)
- [ ] 5.8 Botão "Gerar Checklist" com spinner
- [ ] 5.9 Coluna direita: st.dataframe com preview dos itens
- [ ] 5.10 Botão download Excel (st.download_button)
- [ ] 5.11 Mensagens de erro amigáveis
- [ ] 5.12 Estado da sessão (st.session_state) para persistir resultados

## Trilha 6: Revisão Final (DEPENDE de todas as trilhas)
- [ ] 6.1 Code review: qualidade de código e boas práticas
- [ ] 6.2 Code review: segurança (API keys, injeção, OWASP)
- [ ] 6.3 Code review: UX e usabilidade para público leigo
- [ ] 6.4 Teste funcional com Playwright (navegar, upload, gerar, download)
- [ ] 6.5 Teste com normativo real (Portaria 227)

## Mapa de Dependências
```
Trilha 1 ──┐
Trilha 2 ──┼──> Trilha 5 ──> Trilha 6
Trilha 3 ──┤
Trilha 4 ──┘
```

Trilhas 1-4: PARALELAS (independentes entre si)
Trilha 5: só inicia após 1-4 concluídas
Trilha 6: só inicia após 5 concluída
