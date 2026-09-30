# -*- coding: utf-8 -*-
"""
Gera o Checklist de Etapas do Roteiro de Levantamento (Portaria Secin n. 1/2018).
Planilha passo a passo para execução por equipes sem experiência prévia.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter
import os, copy

PYTHON = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Python", "Python312", "python.exe")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "checklists", "Checklist_Roteiro_Levantamento_Secin_2018_v1.00.xlsx")

# ── Styles ──────────────────────────────────────────────────────────────────
FONT_TITLE   = Font(name="Arial", size=14, bold=True, color="1F4E79")
FONT_H2      = Font(name="Arial", size=12, bold=True, color="1F4E79")
FONT_HDR     = Font(name="Arial", size=10, bold=True, color="FFFFFF")
FONT_NORMAL  = Font(name="Arial", size=10)
FONT_BOLD    = Font(name="Arial", size=10, bold=True)
FONT_SMALL   = Font(name="Arial", size=9, color="444444")
FONT_FASE    = Font(name="Arial", size=10, bold=True, color="1F4E79")

FILL_HDR     = PatternFill("solid", fgColor="1F4E79")
FILL_PLAN    = PatternFill("solid", fgColor="D6E4F0")
FILL_EXEC    = PatternFill("solid", fgColor="E2EFDA")
FILL_COM     = PatternFill("solid", fgColor="FCE4D6")
FILL_QC      = PatternFill("solid", fgColor="E4DFEC")
FILL_WHITE   = PatternFill("solid", fgColor="FFFFFF")
FILL_LIGHT   = PatternFill("solid", fgColor="F2F2F2")
FILL_YELLOW  = PatternFill("solid", fgColor="FFF2CC")

ALIGN_WRAP   = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_HDR    = Alignment(horizontal="center", vertical="center", wrap_text=True)

THIN_BORDER  = Border(
    left=Side(style="thin", color="B4B4B4"),
    right=Side(style="thin", color="B4B4B4"),
    top=Side(style="thin", color="B4B4B4"),
    bottom=Side(style="thin", color="B4B4B4"),
)

# ── Phase colors ────────────────────────────────────────────────────────────
PHASE_FILL = {
    "Pré-Planejamento": FILL_YELLOW,
    "Planejamento":     FILL_PLAN,
    "Execução":         FILL_EXEC,
    "Comunicação":      FILL_COM,
    "Controle de Qualidade": FILL_QC,
}

# ── Helper ──────────────────────────────────────────────────────────────────
def style_header_row(ws, row, ncols, font=FONT_HDR, fill=FILL_HDR, align=ALIGN_HDR):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = font
        cell.fill = fill
        cell.alignment = align
        cell.border = THIN_BORDER

def style_data_row(ws, row, ncols, phase=None):
    phase_fill = PHASE_FILL.get(phase, FILL_WHITE)
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = FONT_NORMAL
        cell.alignment = ALIGN_WRAP
        cell.border = THIN_BORDER
        if c == 2:
            cell.fill = phase_fill
            cell.font = FONT_FASE

def write_separator(ws, row, ncols, label, fill):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
    cell = ws.cell(row=row, column=1, value=label)
    cell.font = Font(name="Arial", size=11, bold=True, color="1F4E79")
    cell.fill = fill
    cell.alignment = Alignment(horizontal="center", vertical="center")
    for c in range(1, ncols + 1):
        ws.cell(row=row, column=c).border = THIN_BORDER
        ws.cell(row=row, column=c).fill = fill

# ═══════════════════════════════════════════════════════════════════════════
# SHEET 1: CHECKLIST ETAPA A ETAPA
# ═══════════════════════════════════════════════════════════════════════════

HEADERS_MAIN = [
    "Nº",
    "Fase",
    "Etapa / Atividade",
    "O que fazer (descrição detalhada)",
    "Fonte (§ do Roteiro)",
    "Texto Literal do Roteiro",
    "Entregável / Evidência",
    "Apêndice(s)",
    "Dica Prática",
    "Aplicável a",
    "Status",
    "Observações",
]

# (fase, etapa, descricao, fonte, texto_literal, entregavel, apendice, dica, aplicavel)
# aplicavel: "Ambos" / "Conhecimento" / "Proposição" / "Estudo Viab."
STEPS = [
    # ── PRÉ-PLANEJAMENTO ──
    ("Pré-Planejamento",
     "Definir o tipo de levantamento",
     "Antes de iniciar, a equipe deve definir qual tipo de levantamento será realizado: (a) para aprofundar o conhecimento sobre o objeto de controle, ou (b) para subsidiar a proposição de ações de controle. Cada tipo tem entregas e profundidade de análise distintas.",
     "§§10-14",
     "Compreende-se levantamento como sendo a ação de controle com os seguintes objetivos: a. aprimorar a atuação da Secretaria, aprofundando conhecimentos sobre a Câmara dos Deputados quanto ao funcionamento de suas unidades administrativas e dos respectivos processos de trabalho [...]; e b. subsidiar a proposição de ações de controle.",
     "Decisão documentada sobre o tipo de levantamento",
     "—",
     "Consulte os §§10-14 para entender as diferenças. O tipo (a) é descritivo; o tipo (b) é descritivo e analítico, exigindo avaliação de riscos.",
     "Ambos"),

    ("Pré-Planejamento",
     "Verificar previsão no PACI",
     "Verificar se o levantamento está previsto no Plano Anual de Controle Interno (PACI). Se não estiver, avaliar a conveniência e oportunidade com base em critérios de risco, materialidade, relevância.",
     "§§17-18",
     "A proposta para realização de levantamento deve ser elaborada com base em critérios de risco, materialidade, relevância, conveniência e oportunidade. O levantamento, quando previsível, deve ser incluído no Paci (item 2 do Estatuto da Secin).",
     "Referência ao PACI ou justificativa para demanda não planejada",
     "J",
     "Caso não esteja no PACI, pode ser necessário um Estudo de Viabilidade (Apêndice J) antes de prosseguir.",
     "Ambos"),

    ("Pré-Planejamento",
     "Designar equipe e coordenador",
     "Definir a composição da equipe de levantamento e o coordenador dos trabalhos. Comunicar ao chefe de núcleo ou supervisor.",
     "§§20, 25",
     "Uma medida importante para assegurar que os trabalhos sejam realizados com elevado nível de qualidade é o acompanhamento e a orientação do chefe de núcleo ou supervisor, desde o início do planejamento até a conclusão do relatório.",
     "Ordem de serviço ou designação formal da equipe",
     "B, D",
     "A equipe deve incluir membros com competências complementares. O supervisor acompanha desde o início.",
     "Ambos"),

    ("Pré-Planejamento",
     "Identificar o objeto de controle",
     "Identificar claramente o objeto do levantamento: pode ser uma unidade administrativa, um processo de trabalho ou outro tema específico.",
     "§§1, 10",
     "As unidades administrativas da Câmara dos Deputados e os processos de trabalho por elas executados são passíveis de ações de controle por parte da Secretaria de Controle Interno (Secin). Dessa forma, esses elementos (chamados objetos de controle) compreendem o universo de incidência dessas ações.",
     "Descrição clara do objeto de controle",
     "A",
     "Seja específico: 'Processo de compras da Ditec' é melhor do que 'Ditec'. O objeto guiará todo o restante do trabalho.",
     "Ambos"),

    # ── PLANEJAMENTO ──
    ("Planejamento",
     "Realizar pesquisa exploratória e leituras iniciais",
     "Realizar pesquisas exploratórias de dados, leituras de documentos, identificação de reguladores (normas), entrevistas iniciais com gestores, especialistas e outros atores.",
     "§§21-23",
     "A etapa de planejamento visa compreender o objeto de controle e o ambiente em que está inserido. Durante o planejamento, são realizadas pesquisas exploratórias de dados, leituras de documentos, identificação de reguladores (normas referentes à unidade administrativa, ao processo de trabalho ou ao tema), entrevistas com gestores, especialistas e outros atores, entre outras técnicas de coleta de informações.",
     "Notas de pesquisa, lista de reguladores identificados",
     "E",
     "Use a lista de fontes do §23 (a-m) como checklist: Camaranet, sistemas, legislação, planejamento estratégico, relatórios de gestão, ações anteriores, questionários TCU, notícias, trabalhos acadêmicos, servidores da Secin, gestores, especialistas.",
     "Ambos"),

    ("Planejamento",
     "Consultar fontes de informação",
     "Coletar informações de todas as fontes pertinentes: (a) Camaranet; (b) sistemas informatizados; (c) legislação e normas; (d) planejamento estratégico; (e) relatórios de gestão; (f) ações de controle anteriores; (g) questionários de governança; (h) documentação de atos anteriores; (i) notícias na mídia; (j) trabalhos acadêmicos; (k) servidores da Secin; (l) partes interessadas; (m) especialistas.",
     "§23, a-m",
     "A equipe pode fazer uso, dentre outras, das seguintes fontes de informação: a) Camaranet; b) sistemas informatizados da Casa; c) legislação, regulamentos e normas específicas; d) planejamento estratégico da unidade; e) relatórios de gestão; f) ações de controles anteriores relativas à unidade, processo de trabalho ou tema; g) questionários sobre governança e gestão realizados pela Secin ou pelo TCU; h) documentação referente a atos e fatos administrativos anteriores [...]; i) notícias veiculadas na mídia; j) trabalhos acadêmicos publicados; k) servidores da Secin [...]; l) partes interessadas, servidores e gestores da unidade; e m) especialistas.",
     "Documentação das fontes consultadas e informações obtidas",
     "—",
     "Organize as informações por fonte em uma pasta ou documento. Registre a data de consulta e a referência de cada informação.",
     "Ambos"),

    ("Planejamento",
     "Coletar informações descritivas do objeto",
     "Para o levantamento tipo 'aprofundar conhecimento', coletar informações sobre: reguladores, objetivos, entradas e saídas, recursos de suporte, partes interessadas, direcionadores estratégicos, estrutura organizacional, competências, contexto orçamentário, histórico, processos de trabalho, boas práticas de governança, etc. (lista completa no §46).",
     "§46, a-t",
     "Recomenda-se que sejam coletadas as informações necessárias para a descrição e compreensão do objeto de controle (contexto e funcionamento), tais como: a) reguladores; b) objetivos declarados; c) entradas e saídas; d) recursos de suporte; e) partes interessadas; f) direcionadores estratégicos; g) estratégia de atuação; h) estrutura organizacional; i) competências; j) contexto orçamentário; k) situação do processo na arquitetura de processos; l) histórico da evolução; m) ambientes externo e interno; n) sistemas e processos envolvidos; o) mapas dos principais processos; p) boas práticas; q) aspectos de governança; r) consistência do processo; s) objetivos de sustentabilidade; t) trabalhos acadêmicos.",
     "Dossiê descritivo do objeto com informações de a) até t)",
     "A",
     "Use esta lista (a-t) como checklist de coleta. Nem todos os itens se aplicarão a todos os objetos — use julgamento profissional.",
     "Conhecimento"),

    ("Planejamento",
     "Enviar e-mail de apresentação",
     "Encaminhar e-mail de apresentação da equipe de levantamento ao diretor da unidade administrativa, informando objetivo, composição da equipe e prazo previsto.",
     "§25",
     "As visitas devem ser precedidas de uma reunião de apresentação, previamente agendada, em que a equipe e o coordenador do trabalho expliquem aos gestores e suas equipes os objetivos e a natureza do trabalho de levantamento.",
     "E-mail de apresentação enviado",
     "B",
     "Use o modelo do Apêndice B. Personalize com o nome do diretor, o objeto, os nomes da equipe e o prazo. Aguarde confirmação antes de agendar a reunião.",
     "Ambos"),

    ("Planejamento",
     "Realizar reunião de apresentação com gestores",
     "Agendar e conduzir reunião de apresentação com os gestores e suas equipes, explicando os objetivos e a natureza do levantamento.",
     "§25",
     "Nos levantamentos, é preciso visitar as unidades administrativas da Casa para colher informações, observar procedimentos, inspecionar instalações e validar análises. As visitas devem ser precedidas de uma reunião de apresentação, previamente agendada.",
     "Ata ou registro da reunião de apresentação",
     "—",
     "Prepare uma breve apresentação (slides) com: quem é a equipe, o que é levantamento (não é auditoria!), objetivos, cronograma previsto, o que será necessário dos gestores.",
     "Ambos"),

    ("Planejamento",
     "Realizar entrevistas exploratórias",
     "Conduzir entrevistas (estruturadas, semiestruturadas ou não-estruturadas) com gestores e especialistas. Elaborar roteiro prévio, identificar atores e registrar pontos relevantes por escrito.",
     "§26",
     "Outra técnica de coleta de dados muito utilizada é a entrevista [...]. A equipe deve elaborar o texto e o cronograma de entrevistas, com a identificação dos atores (internos e externos) e finalidade de cada reunião. Os pontos relevantes tratados nas entrevistas devem ser registrados por escrito para posterior revisão, consolidação de informações e supervisão dos trabalhos.",
     "Roteiro de entrevistas, registros escritos dos pontos relevantes",
     "E",
     "Tipos de entrevista: estruturada (roteiro fixo), semiestruturada (roteiro + perguntas livres) ou não-estruturada (livre). Para iniciantes, a semiestruturada é a mais recomendada.",
     "Ambos"),

    ("Planejamento",
     "Agendar visitas técnicas (se necessário)",
     "Agendar visitas técnicas para verificação in loco da operação de processos identificados como relevantes.",
     "§27",
     "A equipe também pode agendar visitas técnicas para verificação in loco da operação de processos identificados como relevantes.",
     "Cronograma de visitas e registros das observações",
     "—",
     "Use um formulário padronizado para registrar observações durante as visitas. Foque nos processos que parecem mais relevantes ou com maior risco.",
     "Ambos"),

    ("Planejamento",
     "Requisitar informações adicionais (se necessário)",
     "Quando necessário, requisitar informações adicionais às unidades para o entendimento do objeto de controle e do seu ambiente.",
     "§28",
     "Quando necessário, a equipe pode requisitar informações adicionais para o entendimento do objeto de controle e do seu ambiente.",
     "E-mail de solicitação de informações enviado",
     "C",
     "Use o modelo do Apêndice C. Seja específico no que está solicitando e estabeleça prazo para resposta.",
     "Ambos"),

    ("Planejamento",
     "Definir técnicas de coleta de dados e diagnóstico",
     "Em conjunto com o Núcleo Setorial de Gestão, escolher as técnicas de coleta e de diagnóstico mais adequadas para os objetivos do trabalho. As técnicas de coleta incluem: entrevista, pesquisa, observação direta, uso de dados existentes. As técnicas de diagnóstico incluem: análise SWOT, DVR, análise de stakeholders, mapeamento de processos, avaliação de riscos, diagrama Ishikawa, árvore de problemas, matriz GUT.",
     "§24",
     "Cabe às equipes de cada levantamento, em conjunto com o Núcleo Setorial de Gestão, aplicar julgamento profissional para escolher as técnicas de coleta de dados e de diagnóstico mais adequadas para os objetivos do trabalho, dando preferência às técnicas corporativas.",
     "Lista de técnicas selecionadas com justificativa",
     "E",
     "Consulte a aba 'Técnicas de Diagnóstico' desta planilha para ver o resumo de cada técnica. Dê preferência às técnicas corporativas da Casa.",
     "Ambos"),

    ("Planejamento",
     "Definir escopo do levantamento",
     "Com base nas informações obtidas, definir o escopo do levantamento. Para 'aprofundar conhecimento': entendimento do objeto e ambiente, descrição dos objetivos, normas, partes interessadas, riscos, problemas, controles, orçamento e sistemas. Para 'subsidiar proposição': acrescentar áreas que deverão ser priorizadas e ações de controle futuras.",
     "§§29, 47, 57-58",
     "Obtidas e sistematizadas as principais informações sobre esse objeto, a equipe, em conjunto com o chefe do núcleo ou coordenador, deve definir o escopo do levantamento.",
     "Documento com escopo definido e aprovado pelo chefe de núcleo",
     "A",
     "O escopo deve ser realista considerando o tamanho da equipe e o prazo disponível. Priorize áreas de maior materialidade, relevância e risco (§47.2).",
     "Ambos"),

    ("Planejamento",
     "Elaborar a Matriz de Planejamento",
     "Sistematizar na Matriz de Planejamento as informações a serem detalhadas na fase de execução, bem como as atividades que nela serão realizadas. A matriz tem 5 colunas: Assunto/Tema/Processo, Informações requeridas, Fontes de informação, Procedimentos de coleta e análise, O que a análise permitirá dizer.",
     "§29",
     "Essa fase é concluída com a elaboração da matriz de planejamento (apêndice A), que sistematiza as informações a serem detalhadas na fase de execução, bem como as atividades que nela serão realizadas.",
     "Matriz de planejamento preenchida",
     "A",
     "A Matriz é o principal papel de trabalho do planejamento. Use o modelo do Apêndice A. Ela terá 5 seções: (1) Visão geral, (2) Detalhamento das áreas prioritárias, (3) Identificação de riscos e controles, (4) Avaliação de riscos, (5) Problemas recorrentes.",
     "Ambos"),

    ("Planejamento",
     "Elaborar cronograma de atividades",
     "Elaborar cronograma detalhado com as atividades de cada fase (planejamento, execução, comunicação), prazos e responsáveis da equipe.",
     "§30",
     "São entregas da fase de planejamento: definição do escopo do levantamento; matriz de planejamento; definição da(s) técnica(s) de coleta de dados e de diagnóstico [...] respectivos procedimentos; e cronograma de atividades do levantamento.",
     "Cronograma de atividades preenchido",
     "D",
     "Use o modelo do Apêndice D. Ele já traz a lista de atividades típicas de cada fase. Distribua as atividades entre os membros da equipe e defina prazos realistas.",
     "Ambos"),

    ("Planejamento",
     "Revisão da Matriz pelo supervisor",
     "Submeter a Matriz de Planejamento ao supervisor/chefe de núcleo para revisão e aprovação antes de iniciar a fase de execução.",
     "§20",
     "Uma medida importante para assegurar que os trabalhos sejam realizados com elevado nível de qualidade é o acompanhamento e a orientação do chefe de núcleo ou supervisor, desde o início do planejamento até a conclusão do relatório.",
     "Matriz de planejamento revisada e aprovada",
     "—",
     "A revisão pelo supervisor é obrigatória. Não avance para a execução sem esta aprovação.",
     "Ambos"),

    # ── EXECUÇÃO ──
    ("Execução",
     "Detalhar e validar informações",
     "Na fase de execução, coletar informações mais detalhadas sobre o objeto e validar o entendimento obtido na fase de planejamento junto aos gestores.",
     "§§32-33",
     "Nesta etapa são colhidas informações mais detalhadas e é realizada a validação do entendimento obtido na fase anterior. [...] A etapa de execução consiste na aplicação das técnicas de diagnóstico para compreensão do objeto de controle e seu ambiente, obtenção de dados e validação com o gestor dos resultados alcançados.",
     "Registros de validação com gestores",
     "—",
     "Prepare um resumo do entendimento obtido no planejamento e apresente ao gestor para validação antes de aplicar as técnicas de diagnóstico.",
     "Ambos"),

    ("Execução",
     "Identificar atores e partes interessadas",
     "Identificar os principais atores e partes interessadas do objeto do levantamento, além das atribuições de cada um, possíveis conflitos de interesse e sobreposição de papéis (Análise Stakeholder e Análise RACI).",
     "§49",
     "Nesta fase, são identificados os principais atores e as partes interessadas do objeto do levantamento, além das atribuições de cada um, possíveis conflitos de interesse e sobreposição de papéis (Análise Stakeholder e Análise RACI).",
     "Mapa de stakeholders ou Matriz RACI",
     "E",
     "A análise de stakeholders ajuda a entender quem influencia e quem é influenciado pelo objeto. A Matriz RACI define: Responsável, Aprovador, Consultado, Informado.",
     "Conhecimento"),

    ("Execução",
     "Realizar análise do ambiente — SWOT",
     "Realizar a análise do ambiente interno e externo (Análise SWOT), levantando forças, fraquezas, oportunidades e ameaças que podem afetar o alcance dos objetivos. A partir das fraquezas e ameaças, identificar os riscos mais gerais ou estratégicos.",
     "§50",
     "É também realizada a análise do ambiente interno e externo em que se insere o objeto de controle, levantando as forças, fraquezas, oportunidades e ameaças que podem afetar o alcance dos objetivos pretendidos (Análise SWOT). A partir das fraquezas e ameaças, pode-se identificar os riscos mais gerais ou estratégicos do objeto sob ação de controle.",
     "Matriz SWOT preenchida",
     "E",
     "Faça a SWOT em oficina com os gestores e especialistas. Forças e Fraquezas = ambiente interno; Oportunidades e Ameaças = ambiente externo.",
     "Ambos"),

    ("Execução",
     "Mapear os principais processos de trabalho",
     "Elaborar mapas dos principais processos de trabalho, com entradas, saídas, reguladores e recursos de suporte. Usar preferencialmente a metodologia corporativa de gestão de processos e software como Bizagi.",
     "§§4.1-4.7 do Apêndice E; §53",
     "A técnica de mapeamento de processo fornece uma representação gráfica das operações sob análise, evidenciando a sequência de atividades, os agentes envolvidos, os prazos e o fluxo de documentos. [...] Sempre que possível, deve ser utilizada a metodologia de gestão de processos corporativa.",
     "Mapas de processos validados com gestores",
     "E, G",
     "Nível de detalhe depende do escopo. Para visão macro: macroprocessos. Para análise detalhada: fluxograma com atividades, decisões e documentos. Valide sempre com o gestor (§4.3).",
     "Ambos"),

    ("Execução",
     "Avaliar controles internos da gestão (COSO)",
     "Avaliar os controles internos da gestão nos níveis da unidade administrativa e dos processos de trabalho, com base no modelo COSO (2013): Ambiente de Controle, Avaliação de Risco, Atividades de Controle, Informação e Comunicação, Monitoramento.",
     "§§5.1-5.5 do Apêndice E",
     "A avaliação dos controles internos da gestão pode ser realizada na fase de execução do levantamento e possui dois níveis de detalhamento: unidade administrativa e processos de trabalho. [...] Uma avaliação objetiva do desenho e da implementação dos controles internos da gestão deve se basear em uma estrutura razoável de critérios, como a disponibilizada pelo Controle Interno — Estrutura Integrada (Coso Icif, 2013).",
     "Relatório de avaliação dos controles internos (5 componentes COSO)",
     "E, F",
     "Consulte a aba 'Controles Internos COSO' para ver os 17 princípios e seus atributos. Valide as informações com os gestores antes de concluir (§5.5.1). Esta avaliação é altamente recomendável para levantamentos com avaliação de riscos (§5.5.2).",
     "Ambos"),

    ("Execução",
     "Aplicar técnicas de diagnóstico selecionadas",
     "Aplicar as técnicas de diagnóstico definidas no planejamento: análise SWOT, DVR (determinação do nível de risco), análise de stakeholders, mapeamento de processos, avaliação de riscos, Ishikawa, árvore de problemas, Matriz GUT, entre outras.",
     "§§33, 48",
     "A etapa de execução consiste na aplicação das técnicas de diagnóstico para compreensão do objeto de controle e seu ambiente, obtenção de dados e validação com o gestor dos resultados alcançados. Permite também a interpretação e sistematização das informações coletadas nas etapas iniciais do levantamento.",
     "Documentação das técnicas aplicadas e seus resultados",
     "E",
     "A extensão e profundidade variam conforme o objetivo do levantamento (§34). Para 'subsidiar proposição', são obrigatórias a avaliação de riscos ou análise de problemas.",
     "Ambos"),

    ("Execução",
     "Identificar e avaliar riscos",
     "Identificar eventos de risco que possam impedir ou dificultar o alcance dos objetivos. Analisar os riscos em termos de probabilidade de ocorrência e impacto (consequências). Registrar cada risco com: evento, causas e consequências. Classificar como inerente ou residual.",
     "§§5.1-18 do Apêndice E; §59.1",
     "A avaliação de riscos é iniciada pela identificação dos riscos a partir do entendimento do objeto de controle, respectivos objetivos e seu ambiente, incluindo os controles internos da gestão. É concluída com a verificação das respostas da gestão aos riscos identificados. [...] Os riscos identificados devem ser registrados em sistema ou papel de trabalho, tais como planilhas ou matriz de avaliação de riscos. Cada risco deve ser descrito separadamente e deve ser decomposto, no mínimo, nos seguintes componentes: evento, causas e consequências.",
     "Matriz de avaliação de riscos (evento, causas, consequências, probabilidade, impacto, nível de risco)",
     "E",
     "Use a abordagem top-down (§12): do nível geral da unidade para o nível das atividades. Considere riscos operacionais, de conformidade, de informação e de fraude. Consulte gestores sobre as estimativas de impacto e probabilidade (§17.2).",
     "Proposição"),

    ("Execução",
     "Realizar análise de problemas (se aplicável)",
     "Aplicar técnicas de análise de problemas para identificar e estudar em profundidade um problema central, suas causas, consequências e inter-relações. Utilizar diagrama Ishikawa, árvore de problemas ou Matriz GUT.",
     "§§19.1-19.5 do Apêndice E; §59.2",
     "A análise de problemas auxilia o estudo em profundidade e de forma estruturada de problemas, fornecendo subsídios para a identificação de suas causas, suas consequências, suas inter-relações, assim como possíveis soluções. [...] As técnicas de análise de problemas são aplicadas com o objetivo de identificar e estudar um problema considerado central em relação ao objeto sob levantamento, assim como suas causas.",
     "Diagrama de causa-efeito ou árvore de problemas preenchida",
     "E",
     "O Ishikawa (espinha de peixe) e a árvore de problemas são complementares. O Ishikawa identifica causas; a árvore organiza causas e efeitos. A Matriz GUT prioriza as causas por Gravidade, Urgência e Tendência.",
     "Proposição"),

    ("Execução",
     "Propor ações de controle futuras",
     "A partir dos riscos residuais e problemas identificados, indicar as ações de controle a serem propostas. Considerar o conjunto dos riscos, pois uma única ação pode cobrir diversos riscos.",
     "§§18, 57, 62",
     "A partir dos riscos residuais, a equipe de levantamento pode iniciar o trabalho de identificação das ações de controle a serem propostas. Na sugestão de ações de controle, é importante que a equipe considere o conjunto dos riscos identificados, pois é possível que uma única ação de controle possa ser sugerida para diversos riscos apontados.",
     "Lista de ações de controle propostas (objeto e modalidade)",
     "—",
     "Para cada ação proposta, indique: o objeto da ação, a modalidade (auditoria, monitoramento, etc.), justificativa baseada nos riscos identificados, e benefícios esperados.",
     "Proposição"),

    ("Execução",
     "Documentar e validar técnicas com gestores",
     "Ao terminar a execução, as técnicas de diagnóstico devem estar concluídas, documentadas e validadas com o gestor. O ideal é validar em reunião.",
     "§35",
     "Terminada a etapa de execução, as técnicas de diagnóstico devem estar concluídas, documentadas e validadas com o gestor. O ideal é que as técnicas de diagnóstico sejam validadas junto com os gestores em reunião. Nesses casos, a equipe pode fazer um esboço prévio das técnicas a aplicar.",
     "Ata de reunião de validação com gestores",
     "—",
     "Prepare um esboço prévio e apresente em reunião ao gestor. Registre concordância ou ajustes em ata.",
     "Ambos"),

    ("Execução",
     "Realizar reunião de encerramento",
     "Conduzir reunião de encerramento, quando os auditores e o coordenador apresentam aos gestores as principais conclusões e agradecem pela colaboração.",
     "§36",
     "O fim da etapa de execução é marcado pela reunião de encerramento, quando os auditores e o coordenador do levantamento apresentam aos gestores as principais conclusões e agradecem pela colaboração durante a realização do trabalho.",
     "Ata da reunião de encerramento",
     "—",
     "Prepare uma apresentação breve com as principais conclusões. Não entre em detalhes de recomendações (levantamento não faz recomendações — §15).",
     "Ambos"),

    # ── COMUNICAÇÃO ──
    ("Comunicação",
     "Elaborar a Introdução do relatório",
     "Redigir a introdução contendo: previsão no PACI e razões; identificação do objeto; objetivos e limites; escopo e unidades abrangidas; ações de controle anteriores; técnicas utilizadas; limitações; declaração de conformidade com o Estatuto e Roteiro da Secin.",
     "§38, 38.1-38.8",
     "A introdução deve conter as seguintes informações, apresentadas de forma concisa, em texto contínuo, sem subtítulos: 38.1. a previsão do levantamento e as razões que a originaram; 38.2. a identificação do objeto de controle; 38.3. os objetivos e limites do trabalho; 38.4. o escopo [...]; 38.5. as ações de controle anteriores da Secin ou do TCU [...]; 38.6. as técnicas utilizadas [...]; 38.7. a indicação clara daquilo que não pôde ser verificado em profundidade suficiente [...]; 38.8. a declaração de que 'o trabalho foi conduzido em conformidade com o Estatuto da Secin e com o Roteiro de Levantamento da Secin, e que está alinhado com os princípios fundamentais de auditorias do setor público das Normas Internacionais do IIA'.",
     "Seção 1 (Introdução) do relatório redigida",
     "K, L",
     "Escreva em texto contínuo, SEM subtítulos. Inclua obrigatoriamente a declaração do §38.8. Use o modelo do Apêndice K ou L conforme o tipo de levantamento.",
     "Ambos"),

    ("Comunicação",
     "Elaborar a Visão Geral do Objeto",
     "Descrever as características necessárias ao entendimento do objeto e seu ambiente: objetivos, direcionadores estratégicos, normativos básicos, riscos identificados, controles internos, orçamento, sistemas, processos, boas práticas, fontes de evidência.",
     "§39",
     "Na visão geral do objeto, são descritas as características necessárias ao entendimento do objeto de controle e seu ambiente, abrangendo objetivos, direcionadores estratégicos, normativos básicos, riscos anteriormente identificados, controles internos da gestão, aspectos orçamentários, sistemas e processos de trabalho e atividades relacionadas, boas práticas de governança e de gestão identificadas, bem como as possíveis fontes de evidência de futuras ações de controle.",
     "Seção 2 (Visão Geral) do relatório redigida",
     "K, L",
     "Para o tipo 'aprofundar conhecimento', o desenvolvimento do relatório CORRESPONDE à visão geral do objeto (§52). Para 'subsidiar proposição', a visão geral é uma seção separada.",
     "Ambos"),

    ("Comunicação",
     "Elaborar o Desenvolvimento do relatório",
     "Para 'aprofundar conhecimento': o desenvolvimento é a própria visão geral, com subseções por processo (aspecto organizacional, reguladores, TI, orçamentário, boas práticas, riscos, controles internos). Para 'subsidiar proposição': detalhar áreas prioritárias com avaliação de riscos e análise de problemas.",
     "§§40, 52, 61",
     "O conteúdo do desenvolvimento e a quantidade de capítulos variarão de acordo com o objetivo do levantamento. [...] O desenvolvimento do relatório corresponde à própria visão geral do objeto [para tipo conhecimento]. [...] No desenvolvimento do relatório [tipo proposição], detalham-se as áreas prioritárias (processos ou atividades) em que foram realizadas a avaliação de risco ou a análise de problemas.",
     "Seção 3 (Desenvolvimento) do relatório redigida",
     "K, L",
     "Siga a estrutura dos Apêndices K ou L. Para cada processo mapeado, inclua subseções: organizacional, reguladores, TI, orçamento, pontos fortes/fracos, controles, riscos.",
     "Ambos"),

    ("Comunicação",
     "Elaborar Proposta de Encaminhamento (se tipo 'proposição')",
     "Para o tipo 'subsidiar proposição': redigir seção específica com as ações de controle propostas, indicando objeto e modalidade. O despacho do coordenador segue modelo padrão do §62.",
     "§62",
     "As ações de controle propostas figuram em item específico do relatório. Nesse caso, o despacho padrão do coordenador do levantamento pode seguir o seguinte modelo: 'Manifesto minha concordância com a proposta de encaminhamento da equipe de levantamento. Encaminho ao Secretário de Controle Interno o presente relatório para manifestação quanto à conveniência e oportunidade de realização das ações propostas, bem como quanto à inclusão no Plano Anual de Controle Interno.'",
     "Seção 4 (Proposta de Encaminhamento) do relatório redigida",
     "L",
     "Cada ação proposta deve ter: objeto, modalidade (auditoria, levantamento, etc.), justificativa baseada nos riscos e problemas identificados.",
     "Proposição"),

    ("Comunicação",
     "Elaborar a Conclusão",
     "Redigir a conclusão respondendo ao objetivo do levantamento, com referências aos itens do relatório. Para 'aprofundar': relato resumido destacando pontos mais importantes. Para 'proposição': considerações gerais e justificativas para as ações propostas.",
     "§§42, 52, 63",
     "A conclusão deve responder ao objetivo do levantamento, fazendo referências aos itens do relatório nas quais se baseia. [...] Para aprofundar: a conclusão trará um relato resumido do trabalho realizado, destacando os pontos mais importantes do objeto sob ação de controle. [...] Para proposição: a conclusão deverá conter as considerações gerais sobre o trabalho realizado e as justificativas para a realização de outras ações.",
     "Seção 5 (Conclusão) do relatório redigida",
     "K, L",
     "Não introduza informações novas na conclusão. Registre agradecimento à unidade pela colaboração. Inclua assinaturas da equipe, chefe de núcleo e secretário.",
     "Ambos"),

    ("Comunicação",
     "Incluir apêndices e anexos",
     "Incluir como apêndices do relatório: técnicas de diagnóstico utilizadas, matriz de planejamento e resultados das técnicas selecionadas. Preparar documentação complementar para compreensão clara das conclusões.",
     "§§43, 64",
     "Nos apêndices e anexos, a equipe deve preparar a documentação que forneça uma compreensão clara das conclusões do levantamento e da visão geral do objeto. No apêndice do relatório, deverão figurar as técnicas de diagnóstico utilizadas e a matriz de planejamento.",
     "Apêndices do relatório montados",
     "—",
     "Organize os apêndices na ordem em que são referenciados no texto. Inclua a Matriz de Planejamento e as técnicas de diagnóstico obrigatoriamente.",
     "Ambos"),

    ("Comunicação",
     "Arquivar papéis de trabalho",
     "Analisar todos os papéis de trabalho que não foram incluídos no processo e arquivá-los caso sejam considerados importantes.",
     "§44",
     "Ao final do levantamento, todos os papéis de trabalho que não foram incluídos no processo (como documentos que fundamentam a visão geral do objeto) deverão ser analisados e arquivados pela equipe de auditoria, caso sejam considerados importantes para fornecer compreensão clara do trabalho realizado.",
     "Papéis de trabalho organizados e arquivados",
     "—",
     "Crie uma estrutura de pastas: /Planejamento, /Execução, /Comunicação, /Papéis de Trabalho. Guarde tudo que possa ser útil em trabalhos futuros.",
     "Ambos"),

    # ── CONTROLE DE QUALIDADE ──
    ("Controle de Qualidade",
     "Preencher formulário de qualidade — Equipe",
     "A equipe preenche o formulário de controle de qualidade (Apêndice H), verificando se as atividades mais importantes foram realizadas. O formulário avalia: aspectos gerais, planejamento, execução e comunicação.",
     "§67",
     "A equipe de levantamento pode utilizar o formulário disponível no Apêndice H para verificar se as atividades mais importantes do trabalho foram realizadas.",
     "Formulário de controle de qualidade — equipe preenchido",
     "H",
     "Use escala de 1 a 5: (1) discordo totalmente; (2) discordo; (3) neutro; (4) concordo; (5) concordo totalmente; n/a) não se aplica. Justifique itens com nota abaixo de 3.",
     "Ambos"),

    ("Controle de Qualidade",
     "Preencher formulário de qualidade — Supervisor",
     "O revisor (supervisor) preenche o formulário de controle de qualidade (Apêndice I), assegurando que os requisitos do roteiro foram seguidos. Avalia: informações gerais, papéis de trabalho, relatório e resultados do trabalho.",
     "§68",
     "Por sua vez, o revisor deverá assegurar que os requisitos definidos no roteiro de levantamento da Secin foram seguidos, preenchendo o formulário de controle de qualidade disponível no Apêndice I.",
     "Formulário de controle de qualidade — supervisor preenchido, com parecer do Secretário",
     "I",
     "O supervisor avalia: Matriz de Planejamento, redação, concisão e consistência do relatório, e se o objetivo foi alcançado (eficácia, economia e eficiência). O Secretário dá parecer final (Aprovado / Aprovado com observações).",
     "Ambos"),
]


# ═══════════════════════════════════════════════════════════════════════════
# SHEET 2: TÉCNICAS DE DIAGNÓSTICO (Apêndice E)
# ═══════════════════════════════════════════════════════════════════════════

TECNICAS_COLETA = [
    ("Técnica de entrevista",
     "Coleta",
     "Coletar informações preliminares; ampliar o conhecimento sobre o objeto e obter a percepção de gestores, especialistas e partes interessadas; obter informação em profundidade; auxiliar na interpretação de dados obtidos por outros métodos.",
     "Quadro 1, Ap. E",
     "Pode ser estruturada (roteiro fixo), semiestruturada (roteiro + livre) ou não-estruturada (livre). Registre pontos relevantes por escrito."),

    ("Técnica de pesquisa",
     "Coleta",
     "Coletar dados por meio de questionários, mediante definição prévia de critérios e indicadores; coletar dados primários não disponíveis em sistemas; obter informações quantitativas e qualitativas.",
     "Quadro 1, Ap. E",
     "Defina claramente os critérios e indicadores antes de elaborar o questionário. Teste com um grupo piloto."),

    ("Técnica de observação direta",
     "Coleta",
     "Coletar dados por meio da observação para compreender determinados aspectos da realidade; ver, ouvir e examinar fatos; coletar informação contextualizada sobre o funcionamento do objeto.",
     "Quadro 1, Ap. E",
     "Use formulário padronizado para registrar observações. Foque nos processos mais relevantes ou com maior risco."),

    ("Uso de dados existentes (secundários)",
     "Coleta",
     "Coletar informações de bancos de dados existentes ou pesquisas já realizadas; realizar cruzamentos com outras técnicas; obter dados quantitativos e qualitativos de forma rápida e barata.",
     "Quadro 1, Ap. E",
     "Avalie a confiabilidade e atualidade dos dados. Retrate as limitações relativas à estrutura dos dados e dificuldades de obtenção."),

    ("Análise SWOT",
     "Diagnóstico",
     "Identificar as forças e fraquezas do ambiente interno e as oportunidades e ameaças do ambiente externo do objeto sob análise.",
     "Quadro 2, Ap. E",
     "Faça em oficina participativa com gestores. Forças/Fraquezas = interno; Oportunidades/Ameaças = externo."),

    ("Diagrama de Verificação de Risco (DVR) — Nível de risco = I × P",
     "Diagnóstico",
     "Identificar riscos e conhecer a capacidade organizacional para seu gerenciamento; avaliar riscos por probabilidade e impacto; identificar partícipes e possíveis objetos de análise futura.",
     "Quadro 2, Ap. E",
     "Parte das fraquezas e ameaças da SWOT. Classifique cada risco por Impacto (1-5) × Probabilidade (1-5). Pode usar a Metodologia Corporativa de Gestão de Riscos (MCGR)."),

    ("Análise de Stakeholders",
     "Diagnóstico",
     "Identificar principais grupos de interesse (partes interessadas); identificar opiniões, conflitos de interesses e informações relevantes.",
     "Quadro 2, Ap. E",
     "Liste todos os atores envolvidos, classifique por influência e interesse, identifique conflitos."),

    ("Mapa de produtos",
     "Diagnóstico",
     "Conhecer os principais objetivos de um processo de trabalho ou unidade administrativa; representar as relações de dependência entre produtos (serviços); identificar os responsáveis.",
     "Quadro 2, Ap. E",
     "Útil para entender a cadeia de valor e as interdependências entre entregas."),

    ("Indicadores de desempenho",
     "Diagnóstico",
     "Aferir resultados quantitativos ou qualitativos; acompanhar e avaliar desempenho ao longo do tempo: anterior vs. corrente, corrente vs. metas, planejado vs. real.",
     "Quadro 2, Ap. E",
     "Verifique se a unidade já possui indicadores definidos. Se não, proponha indicadores relevantes."),

    ("Mapeamento de processos",
     "Diagnóstico",
     "Conhecer o funcionamento de processos de trabalho; identificar boas práticas; identificar oportunidades para racionalização e aperfeiçoamento.",
     "Quadro 2, Ap. E; §§4.1-4.7",
     "Use a metodologia corporativa quando possível. Valide mapas com gestores. Nível de detalhe depende do escopo."),

    ("Avaliação de riscos",
     "Diagnóstico",
     "Identificar eventos de risco; analisar e avaliar riscos por probabilidade e impacto; identificar e avaliar controles internos; identificar/selecionar/definir escopo de possíveis ações de controle.",
     "Quadro 2, Ap. E; §§5.1-18",
     "Abordagem top-down: do nível geral ao específico. Riscos inerentes vs. residuais. 3 passos: objetivos → riscos → controles."),

    ("Diagrama Ishikawa (espinha de peixe / causa-efeito)",
     "Diagnóstico",
     "Diferenciar causas dos efeitos de um problema; representar graficamente as possíveis causas que levam a um determinado efeito.",
     "Quadro 2, Ap. E",
     "Use as categorias clássicas: Pessoas, Processos, Tecnologia, Regulação (ou 6M). Faça em grupo com os envolvidos."),

    ("Árvore de Problemas",
     "Diagnóstico",
     "Identificar o problema central e organizar causas e consequências/efeitos em modelo de relações causais; refletir a inter-relação entre causas e efeitos.",
     "Quadro 2, Ap. E",
     "Coloque o problema central no tronco, causas nas raízes e efeitos nos galhos. Relacione as causas entre si."),

    ("Matriz GUT (Gravidade, Urgência, Tendência)",
     "Diagnóstico",
     "Classificar as causas do problema em termos de Gravidade, Urgência e Tendência; priorizar as causas do problema identificado.",
     "Quadro 2, Ap. E",
     "Pontue de 1 a 5 em cada dimensão. G×U×T dá a prioridade. Comece a tratar pelas maiores pontuações."),
]


# ═══════════════════════════════════════════════════════════════════════════
# SHEET 3: CONTROLES INTERNOS COSO (Apêndice F)
# ═══════════════════════════════════════════════════════════════════════════

COSO_DATA = [
    ("Ambiente de Controle", "1", "A organização demonstra ter comprometimento com a integridade e os valores éticos",
     "1.1 Liderar pelo exemplo — demonstrar valores, filosofia e estilo operacional pelo exemplo da liderança;\n1.2 Estabelecer padrões de conduta por meio de políticas, princípios operacionais e orientações;\n1.3 Avaliar a aderência aos padrões de conduta;\n1.4 Tratar desvios de forma oportuna."),
    ("Ambiente de Controle", "2", "O órgão de governança demonstra independência em relação aos gestores e exerce supervisão",
     "2.1 Estabelecer estrutura de governança;\n2.2 Estabelecer as responsabilidades pela supervisão;\n2.3 Supervisionar os controles internos da gestão;\n2.4 Criar condições para a correção de deficiências."),
    ("Ambiente de Controle", "3", "A administração deve estabelecer estrutura organizacional, atribuir responsabilidades e delegar autoridade",
     "3.1 Estabelecer estrutura organizacional;\n3.2 Estabelecer linhas de subordinação;\n3.3 Definir, atribuir e limitar responsabilidades e delegar autoridade."),
    ("Ambiente de Controle", "4", "A administração deve demonstrar compromisso com a competência ao recrutar, desenvolver e manter pessoas qualificadas",
     "4.1 Estabelecer expectativas de competência;\n4.2 Avaliar a competência e tratar as deficiências;\n4.3 Atrair, desenvolver e manter pessoas capacitadas;\n4.4 Planejar e preparar sucessão e planos de contingência."),
    ("Ambiente de Controle", "5", "A administração faz com que as pessoas assumam responsabilidade por suas funções de controle interno",
     "5.1 Reforçar e manter a responsabilidade das pessoas;\n5.2 Considerar o efeito de pressões excessivas."),
    ("Avaliação de Risco", "6", "A administração deve definir claramente os objetivos e a tolerância ao risco",
     "6.1 Definir objetivos em termos específicos e mensuráveis;\n6.2 Definir tolerância ao risco;\n6.3 Identificar riscos de origem interna ou externa;\n6.4 Envolver os níveis apropriados da administração;\n6.5 Analisar riscos em termos de probabilidade e impacto."),
    ("Avaliação de Risco", "7", "A administração deve tratar os riscos (aceitar, evitar, mitigar, transferir ou compartilhar)", ""),
    ("Avaliação de Risco", "8", "A administração deve considerar o potencial de fraude ao identificar, analisar e tratar riscos",
     "8.1 Considerar os tipos de fraudes que podem ocorrer;\n8.2 Considerar fatores de riscos de fraudes;\n8.3 Tratar os riscos de fraudes."),
    ("Avaliação de Risco", "9", "A administração deve identificar, analisar e responder às mudanças significativas que possam causar impacto nos controles internos",
     "9.1 Identificar as mudanças significativas;\n9.2 Analisar e responder a essas mudanças."),
    ("Atividades de Controle", "10", "A administração deve definir os controles internos da gestão para alcançar os objetivos e tratar os riscos",
     "10.1 Tratar os riscos para o alcance dos objetivos;\n10.2 Definir controles internos da gestão apropriados;\n10.3 Definir controles internos em vários níveis;\n10.4 Considerar a segregação de funções."),
    ("Atividades de Controle", "11", "A administração deve definir e implementar um sistema de informações e controles internos relacionados",
     "11.1 Criar o sistema de informação da entidade;\n11.2 Definir controles internos da gestão apropriados;\n11.3 Definir a infraestrutura de TI do sistema;\n11.4 Definir gestão de segurança do sistema;\n11.5 Definir gestão de TI (aquisição, desenvolvimento e manutenção)."),
    ("Atividades de Controle", "12", "A administração deve implementar os controles internos por meio de políticas e procedimentos",
     "12.1 Documentar as responsabilidades por meio de políticas;\n12.2 Revisar periodicamente os controles internos da gestão."),
    ("Informação e Comunicação", "13", "A administração deve utilizar informações de qualidade para alcançar os objetivos",
     "13.1 Identificar as necessidades de informação;\n13.2 Obter dados relevantes de fontes fidedignas;\n13.3 Transformar dados em informação de qualidade."),
    ("Informação e Comunicação", "14", "A administração deve comunicar internamente as informações necessárias e de qualidade",
     "14.1 Comunicar com toda a organização em todos os níveis;\n14.2 Estabelecer métodos e canais apropriados de comunicação."),
    ("Informação e Comunicação", "15", "A administração deve comunicar externamente as informações necessárias",
     "15.1 Comunicar com as partes interessadas externas;\n15.2 Estabelecer métodos e canais apropriados de comunicação."),
    ("Monitoramento", "16", "A administração deve estabelecer e realizar atividades de monitoramento dos controles internos",
     "16.1 Estabelecer um padrão (linha de base) para monitorar;\n16.2 Monitorar continuamente os controles internos;\n16.3 Realizar avaliações independentes;\n16.4 Avaliar e documentar os resultados do monitoramento."),
    ("Monitoramento", "17", "A administração deve corrigir as deficiências identificadas nos controles internos de forma tempestiva",
     "17.1 Relatar os problemas encontrados;\n17.2 Avaliar os problemas encontrados;\n17.3 Corrigir as deficiências tempestivamente e documentar as ações corretivas."),
]


# ═══════════════════════════════════════════════════════════════════════════
# BUILD WORKBOOK
# ═══════════════════════════════════════════════════════════════════════════

wb = Workbook()

# ────── Sheet 1: Checklist ──────
ws1 = wb.active
ws1.title = "Checklist Etapa a Etapa"
ws1.sheet_properties.tabColor = "1F4E79"

NCOLS = len(HEADERS_MAIN)
COL_WIDTHS = [5, 18, 30, 55, 14, 65, 35, 10, 50, 14, 12, 25]

for i, w in enumerate(COL_WIDTHS, 1):
    ws1.column_dimensions[get_column_letter(i)].width = w

ws1.merge_cells("A1:L1")
c = ws1.cell(row=1, column=1, value="CHECKLIST DE ETAPAS — ROTEIRO DE LEVANTAMENTO DA SECIN (Portaria n. 1/2018)")
c.font = FONT_TITLE
c.alignment = Alignment(horizontal="center", vertical="center")

ws1.merge_cells("A2:L2")
c2 = ws1.cell(row=2, column=1, value="Guia passo a passo para execução de levantamentos pela Secretaria de Controle Interno da Câmara dos Deputados")
c2.font = Font(name="Arial", size=10, italic=True, color="666666")
c2.alignment = Alignment(horizontal="center")

r = 4
for ci, h in enumerate(HEADERS_MAIN, 1):
    ws1.cell(row=r, column=ci, value=h)
style_header_row(ws1, r, NCOLS)

r = 5
current_phase = None
num = 0
for step in STEPS:
    fase, etapa, desc, fonte, texto, entregavel, apendice, dica, aplicavel = step
    if fase != current_phase:
        write_separator(ws1, r, NCOLS, f"▸ FASE: {fase.upper()}", PHASE_FILL.get(fase, FILL_WHITE))
        current_phase = fase
        r += 1
    num += 1
    ws1.cell(row=r, column=1, value=num)
    ws1.cell(row=r, column=2, value=fase)
    ws1.cell(row=r, column=3, value=etapa)
    ws1.cell(row=r, column=4, value=desc)
    ws1.cell(row=r, column=5, value=fonte)
    ws1.cell(row=r, column=6, value=texto)
    ws1.cell(row=r, column=7, value=entregavel)
    ws1.cell(row=r, column=8, value=apendice)
    ws1.cell(row=r, column=9, value=dica)
    ws1.cell(row=r, column=10, value=aplicavel)
    ws1.cell(row=r, column=11, value="")  # Status
    ws1.cell(row=r, column=12, value="")  # Observações
    style_data_row(ws1, r, NCOLS, fase)
    ws1.cell(row=r, column=1).alignment = ALIGN_CENTER
    ws1.cell(row=r, column=5).alignment = ALIGN_CENTER
    ws1.cell(row=r, column=8).alignment = ALIGN_CENTER
    ws1.cell(row=r, column=10).alignment = ALIGN_CENTER
    ws1.cell(row=r, column=11).alignment = ALIGN_CENTER
    ws1.row_dimensions[r].height = 90
    r += 1

ws1.auto_filter.ref = f"A4:{get_column_letter(NCOLS)}{r-1}"
ws1.freeze_panes = "A5"

# ────── Sheet 2: Técnicas ──────
ws2 = wb.create_sheet("Técnicas de Diagnóstico")
ws2.sheet_properties.tabColor = "548235"

HDRS_TEC = ["Nº", "Técnica", "Tipo", "Objetivos", "Fonte", "Dica Prática"]
TEC_WIDTHS = [5, 35, 12, 70, 18, 55]

for i, w in enumerate(TEC_WIDTHS, 1):
    ws2.column_dimensions[get_column_letter(i)].width = w

ws2.merge_cells("A1:F1")
ws2.cell(row=1, column=1, value="TÉCNICAS DE COLETA E DE DIAGNÓSTICO PARA LEVANTAMENTOS (Apêndice E)").font = FONT_TITLE

for ci, h in enumerate(HDRS_TEC, 1):
    ws2.cell(row=3, column=ci, value=h)
style_header_row(ws2, 3, len(HDRS_TEC), fill=PatternFill("solid", fgColor="548235"))

for idx, t in enumerate(TECNICAS_COLETA, 1):
    r = idx + 3
    ws2.cell(row=r, column=1, value=idx)
    ws2.cell(row=r, column=2, value=t[0])
    ws2.cell(row=r, column=3, value=t[1])
    ws2.cell(row=r, column=4, value=t[2])
    ws2.cell(row=r, column=5, value=t[3])
    ws2.cell(row=r, column=6, value=t[4])
    for c in range(1, len(HDRS_TEC) + 1):
        cell = ws2.cell(row=r, column=c)
        cell.font = FONT_NORMAL
        cell.alignment = ALIGN_WRAP
        cell.border = THIN_BORDER
        if t[1] == "Coleta":
            cell.fill = PatternFill("solid", fgColor="E2EFDA")
        else:
            cell.fill = PatternFill("solid", fgColor="D6E4F0")
    ws2.cell(row=r, column=1).alignment = ALIGN_CENTER
    ws2.cell(row=r, column=3).alignment = ALIGN_CENTER
    ws2.row_dimensions[r].height = 70

ws2.auto_filter.ref = f"A3:F{3 + len(TECNICAS_COLETA)}"
ws2.freeze_panes = "A4"

# ────── Sheet 3: COSO ──────
ws3 = wb.create_sheet("Controles Internos COSO")
ws3.sheet_properties.tabColor = "BF8F00"

HDRS_COSO = ["Componente", "Princípio Nº", "Princípio", "Atributos"]
COSO_WIDTHS = [25, 12, 65, 75]

for i, w in enumerate(COSO_WIDTHS, 1):
    ws3.column_dimensions[get_column_letter(i)].width = w

ws3.merge_cells("A1:D1")
ws3.cell(row=1, column=1, value="ESTRUTURA DE CONTROLES INTERNOS — PRINCÍPIOS E ATRIBUTOS (COSO ICIF, 2013)").font = FONT_TITLE

ws3.merge_cells("A2:D2")
ws3.cell(row=2, column=1, value="Fonte: Apêndice F do Roteiro de Levantamento da Secin — Portaria n. 1/2018").font = FONT_SMALL

for ci, h in enumerate(HDRS_COSO, 1):
    ws3.cell(row=4, column=ci, value=h)
style_header_row(ws3, 4, len(HDRS_COSO), fill=PatternFill("solid", fgColor="BF8F00"))

COMP_FILLS = {
    "Ambiente de Controle":     PatternFill("solid", fgColor="D6E4F0"),
    "Avaliação de Risco":       PatternFill("solid", fgColor="E2EFDA"),
    "Atividades de Controle":   PatternFill("solid", fgColor="FCE4D6"),
    "Informação e Comunicação": PatternFill("solid", fgColor="E4DFEC"),
    "Monitoramento":            PatternFill("solid", fgColor="FFF2CC"),
}

for idx, row_data in enumerate(COSO_DATA):
    r = idx + 5
    comp, pnum, princ, attrs = row_data
    ws3.cell(row=r, column=1, value=comp)
    ws3.cell(row=r, column=2, value=pnum)
    ws3.cell(row=r, column=3, value=princ)
    ws3.cell(row=r, column=4, value=attrs)
    fill = COMP_FILLS.get(comp, FILL_WHITE)
    for c in range(1, len(HDRS_COSO) + 1):
        cell = ws3.cell(row=r, column=c)
        cell.font = FONT_NORMAL
        cell.alignment = ALIGN_WRAP
        cell.border = THIN_BORDER
        cell.fill = fill
    ws3.cell(row=r, column=2).alignment = ALIGN_CENTER
    ws3.row_dimensions[r].height = 65

ws3.freeze_panes = "A5"

# ────── Sheet 4: Legenda e Instruções ──────
ws4 = wb.create_sheet("Legenda e Instruções")
ws4.sheet_properties.tabColor = "7030A0"
ws4.column_dimensions["A"].width = 25
ws4.column_dimensions["B"].width = 90

data_leg = [
    ("", "CHECKLIST DE ETAPAS — ROTEIRO DE LEVANTAMENTO DA SECIN", FONT_TITLE),
    ("", "Portaria n. 1, de 4 de dezembro de 2018 — Secretaria de Controle Interno", FONT_H2),
    ("", "Versão 1.00 — 20/02/2026", FONT_BOLD),
    ("", "", None),
    ("OBJETIVO", "Este checklist tem como objetivo guiar, etapa por etapa, a execução de levantamentos realizados pela Secretaria de Controle Interno (Secin) da Câmara dos Deputados, conforme o Roteiro de Levantamento aprovado pela Portaria n. 1/2018. Foi elaborado para ser aplicável por equipes sem experiência prévia com este roteiro.", FONT_NORMAL),
    ("", "", None),
    ("ESTRUTURA", "A planilha contém 4 abas:", FONT_BOLD),
    ("", "1. Checklist Etapa a Etapa — Passo a passo completo com 35 atividades em 5 fases", FONT_NORMAL),
    ("", "2. Técnicas de Diagnóstico — Resumo das 14 técnicas de coleta e diagnóstico (Apêndice E)", FONT_NORMAL),
    ("", "3. Controles Internos COSO — Os 17 princípios e atributos do modelo COSO 2013 (Apêndice F)", FONT_NORMAL),
    ("", "4. Legenda e Instruções — Esta aba", FONT_NORMAL),
    ("", "", None),
    ("COMO USAR", "1. Defina o tipo de levantamento (etapas 1-4: Pré-Planejamento)", FONT_NORMAL),
    ("", "2. Siga as etapas na ordem, preenchendo a coluna 'Status' à medida que concluir cada uma", FONT_NORMAL),
    ("", "3. Use as colunas 'Texto Literal' e 'Dica Prática' para entender exatamente o que o Roteiro exige", FONT_NORMAL),
    ("", "4. Consulte a coluna 'Apêndice(s)' para saber quais modelos utilizar", FONT_NORMAL),
    ("", "5. A coluna 'Aplicável a' indica se a etapa se aplica a Ambos os tipos, apenas a 'Conhecimento' ou apenas a 'Proposição'", FONT_NORMAL),
    ("", "6. Use a coluna 'Observações' para registrar notas e pendências", FONT_NORMAL),
    ("", "", None),
    ("FASES", "", FONT_BOLD),
    ("Pré-Planejamento", "Definições iniciais antes de começar os trabalhos (tipo, PACI, equipe, objeto)", FONT_NORMAL),
    ("Planejamento", "Compreensão do objeto, coleta inicial de informações, definição de escopo e técnicas", FONT_NORMAL),
    ("Execução", "Aplicação das técnicas de diagnóstico, avaliação de riscos e controles, validação com gestores", FONT_NORMAL),
    ("Comunicação", "Elaboração do relatório, apêndices e arquivamento de papéis de trabalho", FONT_NORMAL),
    ("Controle de Qualidade", "Preenchimento dos formulários de qualidade pela equipe e pelo supervisor", FONT_NORMAL),
    ("", "", None),
    ("STATUS", "Sugestão de valores para a coluna Status:", FONT_BOLD),
    ("", "Pendente / Em andamento / Concluído / Não se aplica", FONT_NORMAL),
    ("", "", None),
    ("TIPOS DE LEVANTAMENTO", "", FONT_BOLD),
    ("Conhecimento", "Levantamento para aprofundar o conhecimento sobre o objeto de controle (descritivo — Cap. 4 do Roteiro)", FONT_NORMAL),
    ("Proposição", "Levantamento para subsidiar a proposição de ações de controle (descritivo e analítico — Cap. 5 do Roteiro)", FONT_NORMAL),
    ("Ambos", "Etapas aplicáveis a ambos os tipos de levantamento", FONT_NORMAL),
    ("", "", None),
    ("APÊNDICES DO ROTEIRO", "", FONT_BOLD),
    ("A", "Matriz de planejamento para levantamentos", FONT_NORMAL),
    ("B", "E-mail de apresentação", FONT_NORMAL),
    ("C", "E-mail de solicitação de informações", FONT_NORMAL),
    ("D", "Exemplo de cronograma de atividades", FONT_NORMAL),
    ("E", "Técnicas de coleta e de diagnóstico (ver aba 'Técnicas de Diagnóstico')", FONT_NORMAL),
    ("F", "Estrutura de controles internos COSO 2013 (ver aba 'Controles Internos COSO')", FONT_NORMAL),
    ("G", "Fluxo das atividades de levantamento", FONT_NORMAL),
    ("H", "Formulário de controle de qualidade — equipe", FONT_NORMAL),
    ("I", "Formulário de controle de qualidade — supervisor", FONT_NORMAL),
    ("J", "Estudo de viabilidade da realização de ação de controle", FONT_NORMAL),
    ("K", "Modelo de relatório — aprofundar conhecimento do objeto", FONT_NORMAL),
    ("L", "Modelo de relatório — subsidiar proposição de ações de controle", FONT_NORMAL),
    ("M", "Modelo de relatório — estudo de viabilidade", FONT_NORMAL),
    ("", "", None),
    ("FONTE", "Portaria n. 1, de 4 de dezembro de 2018 — Secretaria de Controle Interno da Câmara dos Deputados.", FONT_NORMAL),
    ("", "Roteiro de Levantamento da Secretaria de Controle Interno (55 páginas, §§1-68, Apêndices A-M).", FONT_NORMAL),
    ("", "Baseado no Roteiro de Levantamento do TCU (Portaria-Segecex n. 24/2018).", FONT_NORMAL),
    ("", "", None),
    ("CHANGELOG", "", FONT_BOLD),
    ("v1.00", "Versão inicial: 35 etapas em 5 fases, 14 técnicas de diagnóstico, 17 princípios COSO.", FONT_NORMAL),
]

for idx, (col_a, col_b, font) in enumerate(data_leg, 1):
    ws4.cell(row=idx, column=1, value=col_a).font = font or FONT_NORMAL
    ws4.cell(row=idx, column=2, value=col_b).font = font or FONT_NORMAL
    ws4.cell(row=idx, column=1).alignment = Alignment(vertical="top")
    ws4.cell(row=idx, column=2).alignment = ALIGN_WRAP
    if font == FONT_BOLD or font == FONT_TITLE or font == FONT_H2:
        ws4.cell(row=idx, column=1).font = font

# ────── Print settings ──────
for ws in [ws1, ws2, ws3]:
    ws.sheet_properties.pageSetUpPr = None
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0

# ────── Save ──────
wb.save(OUT)
print(f"Arquivo salvo: {OUT}")
print(f"Abas: {wb.sheetnames}")
print(f"Etapas no checklist: {num}")
print(f"Técnicas de diagnóstico: {len(TECNICAS_COLETA)}")
print(f"Princípios COSO: {len(COSO_DATA)}")
