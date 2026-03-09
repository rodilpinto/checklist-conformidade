# -*- coding: utf-8 -*-
"""
app.py -- Interface Streamlit para geração de checklists de conformidade normativa.

Integra os módulos de extração de texto (extractor), geração via LLM (llm)
e construção de planilha Excel (excel_builder) em uma interface web simples
voltada para usuários leigos.

Execução:
    cd checklist-app
    streamlit run app.py
"""

from __future__ import annotations

import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from lib.extractor import extract_text
from lib.llm import (
    LLMError,
    RateLimitError,
    TokenLimitError,
    generate_checklist,
    validate_items,
)
from lib.excel_builder import build_excel

# ---------------------------------------------------------------------------
# Configuração da página (DEVE ser a primeira chamada Streamlit)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Checklist de Conformidade",
    page_icon="\u2705",  # check mark como favicon
    layout="wide",
)

# ---------------------------------------------------------------------------
# CSS customizado para melhorar a experiência visual
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Espaçamento mais confortável no topo */
    .block-container {
        padding-top: 2rem;
    }

    /* Estilização dos passos numerados */
    .step-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: #1F4E79;
        color: white;
        font-weight: 700;
        font-size: 16px;
        margin-right: 8px;
        flex-shrink: 0;
    }

    .step-header {
        display: flex;
        align-items: center;
        margin-bottom: 4px;
    }

    .step-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #1A1A2E;
    }

    /* Caixa de orientação com fundo suave */
    .orientation-box {
        background-color: #E8EEF4;
        border-left: 4px solid #1F4E79;
        border-radius: 4px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 0.92rem;
        line-height: 1.5;
        color: #1A1A2E;
    }

    /* Esconder o label padrão do file_uploader quando redundante */
    .stFileUploader > label > div > p {
        font-size: 0.9rem;
    }

    /* Sidebar: instruções com fonte menor */
    section[data-testid="stSidebar"] .sidebar-instructions {
        font-size: 0.85rem;
        line-height: 1.55;
        color: #444;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Carregar variáveis de ambiente (.env na raiz do projeto)
# ---------------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------------
# Inicialização do session_state
# ---------------------------------------------------------------------------
if "checklist_items" not in st.session_state:
    st.session_state["checklist_items"] = None
if "excel_bytes" not in st.session_state:
    st.session_state.excel_bytes = None
if "error" not in st.session_state:
    st.session_state.error = None


# ---------------------------------------------------------------------------
# Sidebar -- Chave de API  (Passo 1)
# ---------------------------------------------------------------------------
def _render_sidebar() -> str:
    """Renderiza a sidebar com campo de API key e retorna a chave configurada."""
    with st.sidebar:
        st.markdown(
            '<div class="step-header">'
            '<span class="step-badge">1</span>'
            '<span class="step-title">Configurar acesso</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-instructions">'
            "Esta ferramenta utiliza o modelo de inteligência artificial "
            "<b>Google Gemini</b> para analisar o normativo. "
            "Para funcionar, é necessário informar uma <b>chave de acesso gratuita</b>."
            "</div>",
            unsafe_allow_html=True,
        )

        env_key = os.getenv("GEMINI_API_KEY", "").strip()

        if env_key:
            st.success("Chave de acesso já configurada. Você pode prosseguir.")

        api_key_input = st.text_input(
            "Chave de acesso (API Key)",
            type="password",
            placeholder="Cole sua chave aqui...",
            help=(
                "A chave é um código alfanumérico fornecido pelo Google. "
                "Se você já possui uma configurada no ambiente (.env), "
                "ela será usada automaticamente."
            ),
        )

        with st.expander("Como obter a chave de acesso (passo a passo)"):
            st.markdown(
                "1. Acesse [aistudio.google.com/apikey](https://aistudio.google.com/apikey)\n"
                "2. Faça login com sua conta Google\n"
                "3. Clique em **Criar chave de API**\n"
                "4. Copie o código gerado e cole no campo acima\n\n"
                "A chave é **gratuita** e não requer cartão de crédito."
            )

        st.divider()

        # Seção "Como funciona"
        st.markdown("**Como funciona esta ferramenta?**")
        st.markdown(
            '<div class="sidebar-instructions">'
            "<b>Passo 1</b> &mdash; Você configura a chave de acesso (acima)<br>"
            "<b>Passo 2</b> &mdash; Envia o normativo (arquivo, texto ou link)<br>"
            "<b>Passo 3</b> &mdash; A IA analisa e gera o checklist automaticamente<br>"
            "<b>Passo 4</b> &mdash; Você revisa e baixa a planilha Excel pronta"
            "</div>",
            unsafe_allow_html=True,
        )

        # Chave digitada manualmente tem prioridade sobre a do ambiente
        return api_key_input.strip() if api_key_input.strip() else env_key


# ---------------------------------------------------------------------------
# Coluna esquerda -- Entrada de dados  (Passo 2)
# ---------------------------------------------------------------------------
def _render_input_column() -> tuple[str | bytes | None, str, str]:
    """Renderiza a coluna de entrada e retorna (source, source_type, extra_prompt).

    Returns:
        Tupla com:
        - source: conteúdo da entrada (bytes para arquivo, str para texto/url, None se vazio)
        - source_type: "pdf", "docx", "text", "url" ou "" se nenhuma entrada
        - extra_prompt: instruções adicionais do usuário
    """
    source = None
    source_type = ""

    st.markdown(
        '<div class="orientation-box">'
        "Escolha <b>uma</b> das três formas abaixo para informar o normativo "
        "(lei, portaria, decreto, resolução etc.) que deseja transformar em checklist."
        "</div>",
        unsafe_allow_html=True,
    )

    tab_upload, tab_text, tab_url = st.tabs(
        ["Enviar arquivo", "Colar texto", "Informar link (URL)"]
    )

    with tab_upload:
        st.markdown(
            "Envie o documento no formato **PDF** ou **Word (.docx)**. "
            "Arquivos escaneados (imagem) não são suportados."
        )
        uploaded_file = st.file_uploader(
            "Selecione o arquivo do normativo",
            type=["pdf", "docx"],
            help="Clique em 'Browse files' ou arraste o arquivo para esta área.",
        )
        if uploaded_file is not None:
            file_ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
            source = uploaded_file.read()
            source_type = file_ext  # "pdf" ou "docx"
            st.caption(f"Arquivo selecionado: **{uploaded_file.name}**")

    with tab_text:
        st.markdown(
            "Copie o texto completo do normativo e cole no campo abaixo. "
            "Quanto mais completo o texto, melhor será o checklist gerado."
        )
        pasted_text = st.text_area(
            "Texto do normativo",
            height=300,
            placeholder=(
                "Cole aqui o texto integral da lei, portaria ou decreto...\n\n"
                "Exemplo:\n"
                "Art. 1º Fica instituída a Política de Governança...\n"
                "Art. 2º Para os efeitos desta Portaria, considera-se..."
            ),
        )
        if pasted_text.strip() and source is None:
            source = pasted_text.strip()
            source_type = "text"

    with tab_url:
        st.markdown(
            "Informe o endereço (link) da página onde o normativo está publicado. "
            "A ferramenta tentará extrair o texto automaticamente."
        )
        url_input = st.text_input(
            "Endereço da página (URL)",
            placeholder="https://www.planalto.gov.br/ccivil_03/...",
            help="Cole o link completo, incluindo https://",
        )
        if url_input.strip() and source is None:
            source = url_input.strip()
            source_type = "url"

    st.markdown("---")

    # Instruções adicionais (abaixo das tabs)
    extra_prompt = st.text_area(
        "Instruções adicionais (opcional)",
        height=100,
        placeholder=(
            "Exemplos de instruções:\n"
            '- "Foque apenas nos artigos sobre proteção de dados pessoais"\n'
            '- "Gere itens separados para o Gestor de Negócio e o Gerente de Projeto"\n'
            '- "Ignore os artigos revogados"'
        ),
        help=(
            "Use este campo para direcionar a análise. "
            "Se deixar em branco, todos os dispositivos do normativo serão analisados."
        ),
    )

    return source, source_type, extra_prompt.strip()


# ---------------------------------------------------------------------------
# Coluna direita -- Resultado  (Passo 3/4)
# ---------------------------------------------------------------------------
def _render_result_column() -> None:
    """Renderiza a coluna de resultado com base no session_state."""

    # Exibir erro, se houver
    if st.session_state.error:
        st.error(st.session_state.error)

    # Se não há itens gerados, exibir mensagem orientadora
    if st.session_state["checklist_items"] is None:
        st.markdown(
            '<div class="orientation-box">'
            "O resultado aparecerá aqui após você enviar o normativo e clicar em "
            "<b>Gerar Checklist</b>.<br><br>"
            "O processo costuma levar entre <b>1 e 3 minutos</b>, dependendo "
            "do tamanho do documento."
            "</div>",
            unsafe_allow_html=True,
        )
        return

    items = st.session_state["checklist_items"]

    # Indicador de sucesso
    st.success(
        f"Checklist gerado com sucesso: **{len(items)} itens** encontrados."
    )

    # Preview em tabela -- selecionar colunas mais relevantes para leitura rápida
    preview_keys = ["artigo", "requisito", "nivel", "responsavel"]
    preview_data = [
        {k: item.get(k, "") for k in preview_keys}
        for item in items
    ]

    st.markdown("**Prévia do checklist** (role para ver todos os itens):")

    st.dataframe(
        preview_data,
        column_config={
            "artigo": st.column_config.TextColumn("Artigo/Dispositivo", width="small"),
            "requisito": st.column_config.TextColumn("O que deve ser verificado", width="large"),
            "nivel": st.column_config.TextColumn("Prioridade", width="small"),
            "responsavel": st.column_config.TextColumn("Responsável", width="medium"),
        },
        use_container_width=True,
        height=480,
    )

    st.caption(
        "Esta é uma prévia simplificada. A planilha Excel contém todas as colunas "
        "e informações detalhadas de cada item."
    )

    # Botão de download do Excel
    if st.session_state.excel_bytes:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Checklist_Conformidade_{timestamp}.xlsx"

        st.markdown("---")

        st.download_button(
            label="Baixar planilha Excel",
            data=st.session_state.excel_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True,
        )

        st.caption(
            "O arquivo será salvo na pasta de downloads do seu computador. "
            "Abra com Excel, LibreOffice Calc ou Google Planilhas."
        )


# ---------------------------------------------------------------------------
# Lógica principal de geração
# ---------------------------------------------------------------------------
def _generate(source: str | bytes, source_type: str, api_key: str, extra_prompt: str) -> None:
    """Executa o pipeline completo: extração -> LLM -> validação -> Excel.

    Atualiza st.session_state com os resultados ou mensagem de erro.
    """
    # Limpar estado anterior
    st.session_state["checklist_items"] = None
    st.session_state.excel_bytes = None
    st.session_state.error = None

    try:
        # 1. Extrair texto da fonte
        with st.spinner("Etapa 1 de 3: Extraindo o texto do normativo..."):
            text = extract_text(source, source_type)

        if not text or not text.strip():
            st.session_state.error = (
                "Não foi possível extrair texto da fonte fornecida. "
                "Verifique se o arquivo contém texto selecionável "
                "(documentos escaneados como imagem não são suportados). "
                "Se usou um link, verifique se a página contém o texto do normativo."
            )
            return

        # 2. Gerar checklist via LLM
        with st.spinner(
            "Etapa 2 de 3: Analisando o normativo com inteligência artificial... "
            "Isso pode levar de 1 a 3 minutos. Por favor, aguarde."
        ):
            raw_items = generate_checklist(text, api_key=api_key, extra_prompt=extra_prompt)

        # 3. Validar e numerar itens
        with st.spinner("Etapa 3 de 3: Organizando os itens e gerando a planilha..."):
            items = validate_items(raw_items)

            if not items:
                st.session_state.error = (
                    "A análise não encontrou itens de checklist no texto fornecido. "
                    "Verifique se o documento é realmente um normativo com obrigações, "
                    "proibições ou requisitos (ex.: lei, portaria, decreto, resolução)."
                )
                return

            # 4. Gerar planilha Excel
            excel_bytes = build_excel(items, title="Checklist de Conformidade")

        # 5. Persistir no session_state
        st.session_state["checklist_items"] = items
        st.session_state.excel_bytes = excel_bytes

    except RateLimitError:
        st.session_state.error = (
            "O serviço de inteligência artificial está temporariamente sobrecarregado. "
            "Aguarde cerca de 30 segundos e tente novamente."
        )
    except TokenLimitError:
        st.session_state.error = (
            "O normativo é muito extenso para ser processado de uma só vez. "
            "Sugestão: divida o texto em partes menores (por capítulo ou seção) "
            "e gere o checklist de cada parte separadamente."
        )
    except LLMError as exc:
        st.session_state.error = (
            f"Ocorreu um problema na análise do texto: {exc}"
        )
    except ValueError as exc:
        st.session_state.error = (
            f"Problema ao processar os dados: {exc}"
        )
    except RuntimeError as exc:
        st.session_state.error = (
            f"Erro durante o processamento: {exc}"
        )
    except Exception:
        st.session_state.error = (
            "Ocorreu um erro inesperado. Verifique sua conexão com a internet "
            "e tente novamente. Se o problema persistir, entre em contato com "
            "a equipe de suporte técnico."
        )


# ---------------------------------------------------------------------------
# Layout principal
# ---------------------------------------------------------------------------
def main() -> None:
    """Ponto de entrada da aplicação Streamlit."""

    # Título e subtítulo
    st.title("Checklist de Conformidade Normativa")
    st.markdown(
        "Transforme **leis, portarias e decretos** em checklists de auditoria prontos para uso. "
        "Basta enviar o normativo e a ferramenta gera automaticamente uma planilha "
        "com todos os itens que precisam ser verificados."
    )

    st.divider()

    # Sidebar
    api_key = _render_sidebar()

    # Layout em duas colunas
    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown(
            '<div class="step-header">'
            '<span class="step-badge">2</span>'
            '<span class="step-title">Enviar o normativo</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        source, source_type, extra_prompt = _render_input_column()

        # Condições para habilitar o botão
        has_api_key = bool(api_key)
        has_input = source is not None and source_type != ""

        # Botão de geração
        generate_clicked = st.button(
            "Gerar Checklist",
            type="primary",
            disabled=not (has_api_key and has_input),
            use_container_width=True,
        )

        # Mensagens de orientação sobre o botão desabilitado
        if not has_api_key:
            st.warning(
                "Para continuar, configure a chave de acesso na barra lateral "
                "(clique na seta no canto superior esquerdo para abrir).",
                icon="\u2190",
            )
        elif not has_input:
            st.info(
                "Envie um arquivo, cole o texto do normativo ou informe um link "
                "para habilitar o botão acima.",
                icon="\u261D",
            )

    # Executar geração se o botão foi clicado
    if generate_clicked and has_api_key and has_input:
        _generate(source, source_type, api_key, extra_prompt)

    with col_result:
        st.markdown(
            '<div class="step-header">'
            '<span class="step-badge">3</span>'
            '<span class="step-title">Resultado</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        _render_result_column()

    # Rodapé
    _render_footer()


# ---------------------------------------------------------------------------
# Rodapé
# ---------------------------------------------------------------------------
_APP_VERSION = "1.0"

# Estimativa de tempo manual por item de checklist (em minutos).
# Considera: leitura do dispositivo, identificação do requisito,
# análise de risco, definição de responsável, sugestão de evidência
# e mitigação, e preenchimento da planilha.
_MINUTES_PER_ITEM = 8


def _render_footer() -> None:
    """Renderiza o rodapé com versão, autor e estimativa de tempo economizado."""
    items = st.session_state.get("checklist_items")
    num_items = len(items) if items else 0

    if num_items > 0:
        total_min = num_items * _MINUTES_PER_ITEM
        if total_min >= 60:
            hours = total_min // 60
            mins = total_min % 60
            time_str = f"{hours}h{mins:02d}min" if mins else f"{hours}h"
        else:
            time_str = f"{total_min} min"

        savings_html = (
            f'<div style="text-align:center; margin-bottom:6px; '
            f'color:#1F4E79; font-size:0.95rem;">'
            f'<b>{num_items} itens</b> gerados &mdash; '
            f'tempo manual estimado: <b>{time_str}</b> de trabalho economizado'
            f'</div>'
        )
    else:
        savings_html = ""

    st.markdown("---")
    st.markdown(
        f'{savings_html}'
        f'<div style="text-align:center; color:#888; font-size:0.82rem; '
        f'line-height:1.6;">'
        f'Checklist de Conformidade Normativa &mdash; v{_APP_VERSION}<br>'
        f'Feito por <b>Rodrigo Pinto</b> &mdash; '
        f'NUATI / SECIN / C&acirc;mara dos Deputados'
        f'</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
