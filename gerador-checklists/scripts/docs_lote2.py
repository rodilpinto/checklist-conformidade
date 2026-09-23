# -*- coding: utf-8 -*-
"""
docs_lote2.py — Matrizes e Inventários (DOC-03, DOC-06, DOC-12)
"""
from docs_operacionais_helpers import *


def create_doc03():
    """DOC-03: Matriz RACI de Governança de IA"""
    print("DOC-03: Matriz RACI de Governança de IA...")
    wb = new_workbook()
    ws = add_sheet(wb, "Matriz RACI")
    NC = 12  # # | Atividade | Artigo | 9 atores
    set_col_widths(ws, [5, 42, 14, 10, 10, 10, 10, 10, 10, 10, 10, 10])

    r = 1
    write_title_row(ws, r, "MATRIZ RACI DE GOVERNANÇA DE IA", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025 — Arts. 13, 28-37", NC)

    # Legenda RACI
    r += 2
    write_section_header(ws, r, "LEGENDA: R = Responsável | A = Aprovador | C = Consultado | I = Informado", NC)

    # Cabeçalhos de colunas
    r += 1
    atores = [
        "Ditec\n[Art. 29]",
        "Gestores\nde Dados\n[Art. 30]",
        "Gestores\nde Negócio\n[Art. 31]",
        "Gerentes\nde Projeto\n[Art. 32]",
        "Encarregado\nDados Pessoais\n[Art. 33]",
        "CETIA\n[Art. 34]",
        "CDTI\n[Art. 35]",
        "CGE\n[Art. 36]",
        "CGSIC\n[Art. 37]"
    ]
    headers = ["#", "Atividade de Governança", "Artigo(s)"] + atores
    write_col_headers(ws, r, headers, height=50)

    # Atividades de governança derivadas dos artigos
    atividades = [
        # Privacidade (Cap. III)
        ("PRIVACIDADE E PROTEÇÃO DE DADOS", None, None),
        ("Autorizar tratamento de dados pessoais por sistemas de IA",
         "Art. 7º§1º", ["C", "A", "R", "R", "A", "I", "I", "I", ""]),
        ("Autorizar submissão de dados pessoais em nuvem pública",
         "Art. 8º", ["C", "A", "R", "R", "A", "", "", "", ""]),
        ("Garantir anonimização quando necessária",
         "Art. 7º§2º", ["R", "C", "I", "R", "C", "", "", "", ""]),
        ("Vedar uso de e-mail corporativo em IA não contratada",
         "Art. 9º", ["R", "", "I", "I", "", "", "", "", ""]),

        # Transparência (Cap. IV)
        ("TRANSPARÊNCIA", None, None),
        ("Manter explicabilidade e rastreabilidade dos sistemas de IA",
         "Art. 10", ["R", "C", "C", "R", "", "", "", "", ""]),
        ("Prover transparência ao longo do ciclo de vida",
         "Art. 11", ["R", "C", "C", "R", "", "C", "I", "I", ""]),
        ("Informar usuários sobre interação com agente de IA",
         "Art. 12", ["R", "", "R", "R", "", "", "", "", ""]),

        # Responsabilização (Cap. V)
        ("RESPONSABILIZAÇÃO E AUTONOMIA HUMANA", None, None),
        ("Definir papéis e responsabilidades para uso de IA",
         "Art. 13", ["C", "C", "R", "R", "C", "I", "I", "I", ""]),
        ("Verificar conformidade com PG-Dados, POSIC e PDP",
         "Art. 13-Pú", ["C", "C", "R", "", "C", "", "", "", "C"]),
        ("Revisar resultados de IA generativa antes de publicação",
         "Art. 14", ["", "", "R", "R", "", "", "", "", ""]),

        # Resultados Justos (Cap. VI)
        ("RESULTADOS JUSTOS E NÃO DISCRIMINATÓRIOS", None, None),
        ("Verificar vedações de discriminação, vieses e perfilamento",
         "Art. 15", ["R", "", "C", "R", "", "A", "", "", ""]),

        # Robustez e Segurança (Cap. VII)
        ("ROBUSTEZ E SEGURANÇA", None, None),
        ("Realizar testes de robustez dos sistemas de IA",
         "Art. 16", ["R", "", "", "R", "", "", "", "", "C"]),
        ("Assegurar confidencialidade conforme grau de sigilo",
         "Art. 17", ["R", "A", "", "", "", "", "", "", "C"]),
        ("Autorizar tratamento de dados restritos em nuvem privada/infra própria",
         "Art. 18", ["C", "A", "R", "R", "", "", "", "", ""]),
        ("Vedar tratamento de dados restritos em nuvem pública",
         "Art. 19", ["R", "A", "I", "I", "", "", "", "", "C"]),
        ("Definir dados que comprometam processos corporativos",
         "Art. 19§2º", ["", "R", "C", "", "", "", "", "", ""]),

        # Propriedade Intelectual (Cap. VIII)
        ("PROPRIEDADE INTELECTUAL", None, None),
        ("Respeitar propriedade intelectual nos dados utilizados",
         "Art. 20", ["R", "C", "C", "R", "", "", "", "", ""]),
        ("Verificar fontes e indicar autores em documentos gerados por IA",
         "Art. 21", ["", "", "R", "R", "", "", "", "", ""]),

        # Gestão de Riscos (Cap. IX)
        ("GESTÃO DE RISCOS DE IA", None, None),
        ("Considerar ciclo de vida completo na gestão de riscos",
         "Art. 22", ["R", "C", "C", "R", "", "C", "I", "I", ""]),
        ("Definir conjunto mínimo de informações a registrar",
         "Art. 22-Pú", ["R", "", "", "", "", "", "", "", ""]),
        ("Realizar avaliação de riscos éticos e submeter ao CETIA",
         "Art. 24", ["R", "", "I", "I", "C", "A", "I", "I", ""]),
        ("Rejeitar demanda de alto risco e comunicar",
         "Art. 24§2º", ["I", "", "I", "I", "", "R", "I", "I", ""]),
        ("Consultar CGSIC sobre aspectos de segurança",
         "Art. 24§3º", ["C", "", "", "", "", "R", "", "", "A"]),
        ("Encaminhar demandas aprovadas ao CGE para ciência",
         "Art. 24§4º", ["I", "", "", "", "", "I", "R", "A", ""]),
        ("Prover mecanismos de verificação resultados-dados",
         "Art. 25-I", ["R", "", "C", "R", "", "", "", "", ""]),
        ("Recuperar dados de treinamento",
         "Art. 25-II", ["R", "", "", "R", "", "", "", "", ""]),
        ("Armazenar dados externos e RAG para explicação",
         "Art. 25-III", ["R", "", "", "R", "", "", "", "", ""]),
        ("Estabelecer procedimentos por fase do ciclo de vida",
         "Art. 26", ["R", "", "", "C", "", "", "", "", ""]),
        ("Garantir atuação conjunta negócio-Ditec",
         "Art. 26§1º", ["R", "", "R", "R", "", "", "", "", ""]),
        ("Definir responsabilidades para sistemas de terceiros",
         "Art. 26§2º", ["R", "", "R", "R", "", "", "", "", ""]),
        ("Identificar riscos de segurança e plano de testes",
         "Art. 26§3º", ["R", "", "", "R", "", "", "", "", "C"]),
        ("Controlar vieses e alucinações",
         "Art. 26§4º", ["R", "", "C", "R", "", "C", "", "", ""]),

        # Supervisão Contínua (Art. 27)
        ("SUPERVISÃO CONTÍNUA", None, None),
        ("Supervisão contínua compartilhada dos sistemas de IA",
         "Art. 27", ["R", "R", "R", "", "", "", "", "", ""]),
        ("Testes de identificação de riscos éticos",
         "Art. 27§1º", ["R", "C", "C", "", "", "C", "", "", ""]),
        ("Identificar necessidades de ajustes/retreinamento/suspensão",
         "Art. 27§2º", ["R", "R", "R", "", "", "I", "I", "I", ""]),
        ("Monitorar dados contra ataques de segurança",
         "Art. 27§3º", ["R", "C", "I", "", "", "", "", "", "R"]),

        # Papéis específicos (Cap. X)
        ("PAPÉIS ESPECÍFICOS DE GOVERNANÇA", None, None),
        ("Definir e coordenar processo de desenvolvimento de IA",
         "Art. 29-I", ["R", "", "C", "C", "", "", "", "", ""]),
        ("Estabelecer diretrizes de prompts e agentes de IA",
         "Art. 29-II", ["R", "", "I", "I", "", "", "", "", ""]),
        ("Deliberar sobre contratações com IA",
         "Art. 29-III", ["A", "", "R", "", "", "", "C", "I", ""]),
        ("Coordenar gestão de riscos de IA",
         "Art. 29-IV", ["R", "C", "C", "R", "", "C", "", "", ""]),
        ("Coordenar resiliência dos sistemas de IA",
         "Art. 29-V", ["R", "", "", "", "", "", "", "", "C"]),
        ("Subsidiar CETIA, CGE e CDTI com informações",
         "Art. 29-VI", ["R", "", "", "", "", "I", "I", "I", ""]),
        ("Deliberar sobre qualidade dos dados para IA",
         "Arts. 29-VII, 30-III", ["R", "R", "R", "", "", "", "", "", ""]),
        ("Propor retirada de sistema com dados não confiáveis",
         "Art. 30-II", ["I", "R", "C", "", "", "C", "", "", ""]),
        ("Submeter uso contínuo de IA generativa à Ditec",
         "Art. 31-II", ["A", "", "R", "", "", "", "", "", ""]),
        ("Supervisionar processos com IA generativa contínua",
         "Art. 31-III", ["C", "", "R", "", "", "", "", "", ""]),
        ("Suspender IA que não atenda princípios éticos",
         "Art. 31-IV", ["I", "I", "R", "", "", "I", "I", "I", ""]),
        ("Solicitar autorização de dados para projetos de IA",
         "Art. 32-I", ["", "A", "", "R", "C", "", "", "", ""]),
        ("Submeter documentação de IA à Ditec antes do projeto",
         "Art. 32-II", ["A", "", "", "R", "", "", "", "", ""]),
        ("Comunicar periodicamente situação do uso de IA",
         "Art. 32-III", ["I", "", "", "R", "", "", "", "", ""]),
        ("Informar riscos éticos identificados",
         "Art. 32-IV", ["I", "", "", "R", "", "I", "", "", ""]),
        ("Deliberar sobre solicitações de dados pessoais em IA",
         "Art. 33", ["", "", "", "", "R", "", "", "", ""]),
        ("Avaliar relatórios de riscos e emitir parecer",
         "Art. 34-I", ["I", "", "", "", "", "R", "I", "I", ""]),
        ("Avaliar riscos de IA em operação e emitir parecer",
         "Art. 34-II", ["I", "", "", "", "", "R", "I", "I", ""]),
        ("Comunicar pareceres à Ditec, CDTI e CGE",
         "Art. 34-III", ["I", "", "", "", "", "R", "I", "I", ""]),
        ("Emitir relatórios executivos periódicos",
         "Art. 34-IV", ["I", "", "", "", "", "R", "I", "I", ""]),
        ("Considerar análises do CETIA nas demandas TIC",
         "Art. 35", ["C", "", "", "", "", "C", "R", "", ""]),
        ("Deliberar sobre uso, desenvolvimento e contratação de IA",
         "Art. 36", ["C", "", "", "", "", "C", "C", "R", ""]),
        ("Deliberar sobre segurança de IA",
         "Art. 37", ["C", "", "", "", "", "", "", "", "R"]),
    ]

    item = 0
    for atividade in atividades:
        r += 1
        if atividade[1] is None:
            # Cabeçalho de seção
            write_section_header(ws, r, atividade[0], NC)
        else:
            item += 1
            nome, artigo, raci = atividade
            values = [item, nome, artigo] + raci
            fills = [None, None, None] + [fill_yellow()] * 9
            write_data_row(ws, r, values, height=28, fills=fills)
            for col in range(4, NC + 1):
                ws.cell(row=r, column=col).alignment = ALIGN_CENTER
                add_dropdown(ws, ws.cell(row=r, column=col), ["R", "A", "C", "I", ""])

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-03_Matriz_RACI_Governanca_IA.xlsx")


def create_doc06():
    """DOC-06: Glossário Oficial de IA (Art. 2º)"""
    print("DOC-06: Glossário Oficial de IA...")
    wb = new_workbook()
    ws = add_sheet(wb, "Glossário IA")
    NC = 4
    set_col_widths(ws, [5, 28, 80, 14])

    r = 1
    write_title_row(ws, r, "GLOSSÁRIO OFICIAL DE INTELIGÊNCIA ARTIFICIAL", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025 — Art. 2º (transcrição literal)", NC)

    r += 2
    write_col_headers(ws, r, ["#", "Termo", "Definição (texto literal do Art. 2º)", "Inciso"])

    definicoes = [
        ("I", "Inteligência artificial (IA)",
         "tecnologias ou algoritmos capazes de realizar tarefas que normalmente requerem inteligência humana, como aprendizado, reconhecimento de padrões, tomada de decisão, resolução de problemas, compreensão de linguagem natural e interação com o ambiente, fundamentados em dados, regras predefinidas ou aprendizado a partir de experiências"),
        ("II", "Inteligência artificial generativa",
         "modalidade de inteligência artificial capaz de criar novos conteúdos em diversos formatos, como textos, imagens, vídeos, músicas ou outros tipos de mídia, a partir da combinação de padrões aprendidos dos dados em que foi treinada e em novos dados e instruções fornecidos a cada uso"),
        ("III", "Sistemas de inteligência artificial",
         "sistemas ou plataformas digitais que usam a inteligência artificial"),
        ("IV", "Ciclo de vida de sistema de IA",
         "consiste em todas as ações que envolvem desde a concepção do sistema de IA, até a sua desativação, correspondendo às fases de planejamento, desenho e prototipação, coleta e preparação dos dados, modelagem e treinamento, teste e avaliação do modelo, implantação, monitoramento e coleta de feedback, e a desativação"),
        ("V", "Gestor de negócio",
         "titular da unidade administrativa ou colegiado responsável pela visão negocial de soluções de TIC relacionadas a sua área de negócios, nos termos da Portaria nº 88, de 29 de março de 2019"),
        ("VI", "Gestor de dados",
         "titular de unidade ou subunidade administrativa formalmente designado como responsável pelo dado, tendo conhecimento e delegação necessários para tomar quaisquer decisões em relação a esses dados"),
        ("VII", "Princípios éticos aplicados à IA",
         "consenso sobre comportamentos aceitos quando se usa, desenvolve, implementa e contrata sistemas de IA, assim como comportamentos aceitos pelos sistemas de IA"),
        ("VIII", "Alucinação",
         "termo usado na IA generativa para descrever respostas fictícias e convincentes que podem ser erroneamente aceitas por quem não conhece profundamente o assunto"),
        ("IX", "Geração aumentada por recuperação (RAG)",
         "técnica que combina inteligência artificial generativa com sistemas de busca ou mecanismos de recuperação de informações de bases de dados específicas para contextualizar a geração dos resultados, aumentando sua precisão e confiabilidade"),
        ("X", "Agente de IA",
         "sistema de IA que age de forma autônoma ou semiautônoma, a partir da percepção de informações de seu ambiente para atingir objetivos determinados"),
        ("XI", "Dado pessoal sensível",
         "dado pessoal sobre origem racial ou étnica, convicção religiosa, opinião política, filiação a sindicato ou a organização de caráter religioso, filosófico ou político, dado referente à saúde ou à vida sexual, dado genético ou biométrico, quando vinculado a uma pessoa natural, nos termos da Lei nº 13.709, de 14 de agosto de 2018"),
        ("XII", "Nuvem pública para serviços de IA",
         "ambiente de computação operado por provedor externo, baseado em infraestrutura compartilhada, no qual os serviços de IA são processados em plataformas padronizadas do provedor, podendo ocorrer dentro ou fora do território nacional, conforme a arquitetura e configurações ofertadas"),
        ("XIII", "Nuvem privada para serviços de IA",
         "ambiente de computação dedicado e isolado, operado pela organização ou por provedor em regime exclusivo, no qual os serviços e modelos de IA são processados em infraestrutura localizada no território nacional ou em ambientes cuja localização e soberania sejam controladas e definidas pela Câmara dos Deputados"),
    ]

    for i, (inciso, termo, definicao) in enumerate(definicoes, 1):
        r += 1
        write_data_row(ws, r, [i, termo, definicao, inciso], height=55)
        ws.cell(row=r, column=2).font = font_label()
        ws.cell(row=r, column=3).alignment = ALIGN_TOP

    r += 2
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=NC)
    cell = ws.cell(row=r, column=1,
                   value="Nota: Todas as definições foram transcritas literalmente do Art. 2º da "
                         "Portaria 227/2025. Eventuais inconsistências são do texto original publicado "
                         "no Boletim Administrativo.")
    cell.font = font_small()
    cell.alignment = ALIGN_LEFT

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-06_Glossario_Oficial_IA.xlsx")


def create_doc12():
    """DOC-12: Inventário de Dados Restritos"""
    print("DOC-12: Inventário de Dados Restritos...")
    wb = new_workbook()
    ws = add_sheet(wb, "Inventário Dados Restritos")
    NC = 9
    set_col_widths(ws, [5, 22, 20, 20, 16, 20, 14, 14, 22])

    r = 1
    write_title_row(ws, r, "INVENTÁRIO DE DADOS RESTRITOS", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025 — Art. 19, §§1º-3º", NC)

    # Referência normativa
    r += 2
    write_section_header(ws, r, "REFERÊNCIA: Art. 19§1º — Categorias de dados com restrição de acesso", NC)
    r += 1
    categorias_ref = [
        ("a)", "Dados classificados em grau de sigilo com fundamento na segurança da sociedade ou do Estado"),
        ("b)", "Dados protegidos por sigilo legal"),
        ("c)", "Dados cujo acesso coloque os processos corporativos em risco"),
        ("d)", "Dados referentes a credenciais de acesso a sistemas e dispositivos conectados à rede digital"),
    ]
    for letra, desc in categorias_ref:
        r += 1
        ws.cell(row=r, column=1, value=letra).font = font_label()
        ws.cell(row=r, column=1).alignment = ALIGN_CENTER
        ws.cell(row=r, column=1).border = THIN_BORDER
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=NC)
        ws.cell(row=r, column=2, value=desc).font = font_normal()
        ws.cell(row=r, column=2).alignment = ALIGN_LEFT
        ws.cell(row=r, column=2).border = THIN_BORDER
        for c in range(3, NC + 1):
            ws.cell(row=r, column=c).border = THIN_BORDER

    # Identificação
    r += 2
    write_section_header(ws, r, "IDENTIFICAÇÃO", NC)
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
    write_form_field(ws, r, "Unidade administrativa", 1, 3, 5)
    write_form_field(ws, r, "Data de atualização", 6, 7, 9)
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
    write_form_field(ws, r, "Responsável pelo inventário", 1, 3, 5)
    write_form_field(ws, r, "Titular da unidade", 6, 7, 9, ref_artigo="Art. 19§2º")

    # Tabela
    r += 2
    write_section_header(ws, r, "INVENTÁRIO", NC)
    r += 1
    headers = [
        "#",
        "Dado / Conjunto\nde Dados",
        "Unidade\nResponsável",
        "Categoria\nArt. 19§1º",
        "Classificação\nde Sigilo",
        "Sistemas que\nUtilizam",
        "Aprovação\nUso em IA?\n[Art. 18]",
        "Ambiente\nAutorizado",
        "Observações"
    ]
    write_col_headers(ws, r, headers, height=45)

    categorias = [
        "Sigilo de Estado/sociedade",
        "Sigilo legal",
        "Risco a processos corporativos",
        "Credenciais de acesso"
    ]
    classificacoes = ["Ultra-secreto", "Secreto", "Reservado", "Restrito"]
    ambientes = ["Infraestrutura própria apenas", "Nuvem privada", "VEDADO em nuvem pública"]

    for i in range(1, 21):
        r += 1
        fills = [None] + [fill_yellow()] * 8
        write_data_row(ws, r, [i] + [""] * 8, fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=4), categorias)
        add_dropdown(ws, ws.cell(row=r, column=5), classificacoes)
        add_dropdown(ws, ws.cell(row=r, column=7), ["Sim — autorizado", "Não — pendente", "N/A"])
        add_dropdown(ws, ws.cell(row=r, column=8), ambientes)

    # Alerta
    r += 2
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=NC)
    cell = ws.cell(row=r, column=1,
                   value="VEDAÇÃO (Art. 19): É vedado o tratamento de dados com restrição de acesso "
                         "para uso por sistemas de IA em nuvem pública. Inclui minutas de documentos "
                         "restritos (Art. 19§3º).")
    cell.font = Font(name='Arial', size=10, bold=True, color="CC0000")
    cell.fill = PatternFill(start_color="FFF0F0", end_color="FFF0F0", fill_type='solid')
    cell.alignment = ALIGN_LEFT
    cell.border = THIN_BORDER
    for c in range(2, NC + 1):
        ws.cell(row=r, column=c).border = THIN_BORDER
        ws.cell(row=r, column=c).fill = PatternFill(start_color="FFF0F0", end_color="FFF0F0", fill_type='solid')

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-12_Inventario_Dados_Restritos.xlsx")
