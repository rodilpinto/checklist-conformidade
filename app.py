# -*- coding: utf-8 -*-
"""
app.py -- Interface Streamlit para geração de checklists de conformidade normativa.

Integra os módulos de extração de texto (extracao_texto), geração via LLM (llm)
e construção de planilha Excel (excel_builder) em uma interface web simples
voltada para usuários leigos.

Execução:
    cd checklist-app
    streamlit run app.py
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from extracao_texto import extract_text
from lib.llm import (
    LLMError,
    generate_checklist,
    validate_items,
)
import llm_cadeia
from llm_cadeia.painel_streamlit import painel_llm
from lib.excel_builder import build_excel
from branding.streamlit_cd import cd_brand
from tempo_economizado import Etapa, estimar
from tempo_economizado.painel_streamlit import mostrar_tempo_economizado

_APP_TITLE = "Checklist de Conformidade Normativa"

# ---------------------------------------------------------------------------
# Configuração da página (DEVE ser a primeira chamada Streamlit)
# ---------------------------------------------------------------------------
cd_brand.configurar_pagina(_APP_TITLE)

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
        background-color: #2F7958;
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
        color: #414042;
    }

    /* Caixa de orientação com fundo suave */
    .orientation-box {
        background-color: #E5F7EC;
        border-left: 4px solid #2F7958;
        border-radius: 4px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 0.92rem;
        line-height: 1.5;
        color: #414042;
    }

    /* Esconder o label padrão do file_uploader quando redundante */
    .stFileUploader > label > div > p {
        font-size: 0.9rem;
    }

    /* Sidebar: instruções com fonte menor */
    section[data-testid="stSidebar"] .sidebar-instructions {
        font-size: 0.85rem;
        line-height: 1.55;
        color: #414042;
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
def _render_sidebar() -> None:
    """Renderiza a sidebar: acesso à IA (painel do llm_cadeia) e instruções.

    O painel_llm() tem de rodar antes de qualquer chamada ao LLM: ele instala a
    chave que o usuário digitar (vale só na sessão dele) e mostra quem vai responder.
    """
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
            "Esta ferramenta usa <b>inteligência artificial</b> para analisar o normativo. "
            "Os modelos abaixo são tentados em ordem até um responder. "
            "Se quiser, informe <b>sua própria chave</b>: ela tem prioridade e vale só nesta sessão."
            "</div>",
            unsafe_allow_html=True,
        )

        painel_llm()

        st.divider()

        # Seção "Como funciona"
        st.markdown("**Como funciona esta ferramenta?**")
        st.markdown(
            '<div class="sidebar-instructions">'
            "<b>Passo 1</b> &mdash; Confira o acesso à IA (acima)<br>"
            "<b>Passo 2</b> &mdash; Envia o normativo (arquivo, texto ou link)<br>"
            "<b>Passo 3</b> &mdash; A IA analisa e gera o checklist automaticamente<br>"
            "<b>Passo 4</b> &mdash; Você revisa e baixa a planilha Excel pronta"
            "</div>",
            unsafe_allow_html=True,
        )



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
    if st.session_state.get("llm_origem"):
        st.caption(f"Gerado por {st.session_state['llm_origem']}")

    # Preview em tabela -- selecionar colunas mais relevantes para leitura rápida
    preview_keys = ["artigo", "requisito", "probabilidade", "impacto", "nivel", "responsavel"]
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
            "probabilidade": st.column_config.NumberColumn("P", width="small"),
            "impacto": st.column_config.NumberColumn("I", width="small"),
            "nivel": st.column_config.TextColumn("Nível", width="small"),
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
def _generate(source: str | bytes, source_type: str, extra_prompt: str) -> None:
    """Executa o pipeline completo: extração -> LLM -> validação -> Excel.

    Atualiza st.session_state com os resultados ou mensagem de erro.
    """
    # Limpar estado anterior
    st.session_state["checklist_items"] = None
    st.session_state.excel_bytes = None
    st.session_state.error = None
    st.session_state["llm_origem"] = None

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
            raw_items, origem = generate_checklist(text, extra_prompt=extra_prompt)
        st.session_state["llm_origem"] = origem

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

    cd_brand.cabecalho(_APP_TITLE, "Normativos transformados em checklists de auditoria")
    st.markdown(
        "Transforme **leis, portarias e decretos** em checklists de auditoria prontos para uso. "
        "Basta enviar o normativo e a ferramenta gera automaticamente uma planilha "
        "com todos os itens que precisam ser verificados."
    )

    st.divider()

    # Sidebar
    _render_sidebar()

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
        has_access = llm_cadeia.disponivel()
        has_input = source is not None and source_type != ""

        # Botão de geração
        generate_clicked = st.button(
            "Gerar Checklist",
            type="primary",
            disabled=not (has_access and has_input),
            use_container_width=True,
        )

        # Mensagens de orientação sobre o botão desabilitado
        if not has_access:
            st.warning(
                "Nenhum modelo de IA está configurado. Para continuar, informe sua "
                "própria chave de IA na barra lateral "
                "(clique na seta no canto superior esquerdo para abrir).",
                icon="\U0001F448",  # \ud83d\udc48 (o "\u2190" n\u00e3o \u00e9 emoji e levanta StreamlitAPIException)
            )
        elif not has_input:
            st.info(
                "Envie um arquivo, cole o texto do normativo ou informe um link "
                "para habilitar o botão acima.",
                icon="\u261D",
            )

    # Executar geração se o botão foi clicado
    if generate_clicked and has_access and has_input:
        _generate(source, source_type, extra_prompt)
        # Roda de novo para a barra lateral mostrar "Última resposta" (quem gerou).
        st.rerun()

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
_APP_VERSION = "1.1"

# Estimativa de tempo manual (recurso tempo_economizado do nuati-framework): cada etapa que
# um profissional faria à mão, para cada item do checklist, com os minutos de cada vez.
# As 8 etapas somam 9,0 min por item (o comentário antigo dizia 8,0; o número exibido era
# 9,0 × itens e continua o mesmo).
_ETAPAS_MANUAIS = [
    ("Ler e interpretar cada dispositivo legal", 2.0),
    ("Identificar o requisito de conformidade de cada item", 1.0),
    ("Avaliar probabilidade e impacto de cada item (MCGR)", 1.5),
    ("Calcular a criticidade e classificar o nível de cada item", 1.0),
    ("Definir o responsável pelo atendimento de cada item", 0.5),
    ("Elaborar a sugestão de mitigação de cada item", 1.5),
    ("Identificar a evidência comprobatória de cada item", 1.0),
    ("Preencher e formatar cada item na planilha", 0.5),
]


def _render_footer() -> None:
    """Renderiza o rodapé com a estimativa de tempo economizado e a assinatura da Câmara."""
    items = st.session_state.get("checklist_items")
    num_items = len(items) if items else 0

    st.markdown("---")

    # Sem descontar o tempo da ferramenta (automatico_min=0), como a conta anterior.
    est = estimar([Etapa(descricao, num_items, minutos) for descricao, minutos in _ETAPAS_MANUAIS])
    mostrar_tempo_economizado(est)

    cd_brand.rodape()
    st.markdown(
        f'<div style="text-align:right; color:#6D6C6F; font-size:0.78rem;">'
        f'{_APP_TITLE} v{_APP_VERSION} &middot; Feito por Rodrigo Pinto'
        f'</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
