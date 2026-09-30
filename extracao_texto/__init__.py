"""extracao_texto: texto de PDF, DOCX, URL (com protecao SSRF) ou texto colado. Comece pelo README.md.

    from extracao_texto import extract_text
    texto = extract_text(arquivo.read(), "pdf")      # "pdf" | "docx" | "url" | "text"

Pasta copiavel: a ORIGEM vive em github.com/rodilpinto/nuati-framework, pasta extracao_texto/.
Nao edite uma copia: melhore a origem, suba __version__ e recopie.
"""

from .extractor import extract_from_docx, extract_from_pdf, extract_from_url, extract_text

__version__ = "1.0.0"

__all__ = ["extract_text", "extract_from_pdf", "extract_from_docx", "extract_from_url", "__version__"]
