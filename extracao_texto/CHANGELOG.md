# Changelog do extracao_texto

Versão atual em `__init__.py` (`__version__`).

## 1.0.0 (30/09/2026): entra no nuati-framework

`extractor.py` trazido **sem mudança** de `checklist-conformidade`, branch `feat/llm-cadeia` @ `92ac158` (servidor
interno), `lib/extractor.py` (mesmo hash git: `7013a4a`). Novos: `__init__.py` (versão e as 4 funções públicas),
`README.md`, este changelog e `test_extracao_texto.py` (28 testes sem rede: PDF e DOCX gerados em memória; bloqueios
SSRF, domínio confiável, redirecionamento revalidado, limites de tamanho, com DNS e `requests` dublados).

Um teste `xfail` registra um defeito achado ao ler o código, não corrigido nesta versão (sem mudança de código): o
redirecionamento relativo sem barra inicial. Pendências no README.

Por que este e não os outros (levantamento de 29/09, 📝 avaliação da sessão do levantamento, conferida aqui na
leitura): cobre os 3 formatos e tem a proteção SSRF mais completa. O `input_parser.py` do scopediagram (pypdf, sem
URL) e o SSRF do `google_searcher.py` do buscador (só URL; não comparado linha a linha, nem pelo levantamento nem
aqui) ficam nos apps até o passe
por app.
