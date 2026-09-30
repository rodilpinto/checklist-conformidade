# extracao_texto: texto de PDF, DOCX, URL ou texto colado (pasta copiável)

**Versão 1.0.0** · **Origem:** `github.com/rodilpinto/nuati-framework` (privado), pasta `extracao_texto/`.
Histórico: [`CHANGELOG.md`](CHANGELOG.md). Regras de cópia e registro de onde há cópias: README da raiz do framework.

Recebe o que o usuário enviou (bytes do `st.file_uploader`, uma URL ou texto colado) e devolve texto limpo em UTF-8,
pronto para ir ao LLM. Veio do `checklist-conformidade` (`lib/extractor.py`), o mais completo dos extratores do
levantamento de 29/09.

## Usar

```python
from extracao_texto import extract_text

texto = extract_text(arquivo.read(), "pdf")     # bytes: "pdf" ou "docx"
texto = extract_text("https://...", "url")      # str
texto = extract_text(colado, "text")            # str
```

| Fonte | Como | Observação |
|---|---|---|
| PDF | PyMuPDF, página a página | marcador `--- Pagina N ---` entre páginas; PDF escaneado (só imagem) devolve `""`: precisa de OCR, que não está aqui |
| DOCX | python-docx | parágrafos e depois as tabelas, célula `a \| b` por linha |
| URL | requests + BeautifulSoup | tira `script`, `style`, `noscript`, `svg`, `canvas`; devolve o texto do `<body>` |
| texto | `strip()` | n/a |

Erros: `ValueError` para entrada inválida ou bloqueada (tipo errado, URL perigosa, arquivo grande demais);
`RuntimeError` para falha ao ler (PDF corrompido, HTTP 404, tempo esgotado). O app decide a mensagem.

## Limites e proteções

| Proteção | Valor | Onde |
|---|---|---|
| Tamanho de PDF/DOCX | 50 MB | `_MAX_FILE_SIZE_BYTES` |
| Tamanho de resposta HTTP | 10 MB (pelo `Content-Length` e contando o que chega) | `_MAX_RESPONSE_SIZE_BYTES` |
| Texto devolvido | 500.000 caracteres (corta na última palavra) | `_MAX_EXTRACTED_CHARS` |
| Tempo por requisição | 30 s | `_REQUEST_TIMEOUT_SECONDS` |
| Redirecionamentos | até 5, **cada destino revalidado** | `extract_from_url` |

**Proteção SSRF** (impedir que uma URL digitada pelo usuário faça o servidor acessar a rede interna): só `http`/`https`;
bloqueia `localhost`, `metadata.google.internal` e qualquer host que resolva para IP privado, loopback, link-local ou
reservado (inclui o `169.254.169.254` de metadados de nuvem); host que não resolve é bloqueado. Exceção: domínios
confiáveis passam mesmo resolvendo para IP privado (DNS interno), padrão `camara.leg.br`, troque com a variável de
ambiente `EXTRACTOR_TRUSTED_DOMAINS` (lista separada por vírgula; ela **substitui** o padrão).

## Adotar num app

1. **Copie a pasta inteira** `extracao_texto/` para a raiz do app, sem editar nada, e registre a cópia no README da
   raiz do framework ("Registro de cópias").
2. **Dependências** no `requirements.txt`: `pymupdf`, `python-docx`, `requests`, `beautifulsoup4` (opcional:
   `chardet`, para adivinhar a codificação de páginas sem charset).
3. Troque o extrator do app por `extract_text`. No checklist: `from lib.extractor import ...` vira
   `from extracao_texto import ...` (mesmas funções). No scopediagram (`input_parser.py`, usa `pypdf`): arquivo
   `.txt/.md/.csv/.json` → decodifique em UTF-8 e use `"text"`; `.pdf`/`.docx` → `"pdf"`/`"docx"`. ⚠ O texto do PDF
   pode sair diferente do `pypdf` (outro motor, e com marcadores de página): confira o prompt do app com um arquivo
   real antes de publicar.
4. Rode, da pasta que contém `extracao_texto/`: `python -m pytest extracao_texto -q`.

## Pendências conhecidas (1.0.0)

- ⚠ Redirecionamento relativo **sem** barra inicial (`Location: b.html`) não é resolvido contra a URL atual e falha
  como URL inválida. Teste marcado `xfail` em `test_extracao_texto.py`. 📝 Conserto sugerido: `urllib.parse.urljoin`.
- 📝 A validação resolve o DNS e depois o `requests` resolve de novo: um DNS malicioso poderia responder diferente na
  segunda vez (*DNS rebinding*). Fechar isso exige fixar o IP resolvido na conexão; não feito.
- 📝 A PyMuPDF 1.28 avisa que `import fitz` está obsoleto (usar `import pymupdf`); ainda funciona.

## Regra de sincronia

**Não edite uma cópia.** Melhoria nasce no framework, sobe `__version__`, entra no `CHANGELOG.md` e é recopiada.
