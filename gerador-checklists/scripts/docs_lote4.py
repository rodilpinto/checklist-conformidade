# -*- coding: utf-8 -*-
"""
docs_lote4.py — Termos e Templates de Relatório (DOC-08, DOC-09, DOC-13, DOC-14)
"""
from docs_operacionais_helpers import *


def create_doc08():
    """DOC-08: Termo de Ciência e Uso Responsável de IA (.docx)"""
    print("DOC-08: Termo de Ciência e Uso Responsável de IA...")
    doc = new_document(
        "TERMO DE CIÊNCIA E USO RESPONSÁVEL DE INTELIGÊNCIA ARTIFICIAL",
        "Política de Governança de IA — Portaria 227/2025"
    )

    add_docx_section(doc, "1. PREÂMBULO")
    add_docx_paragraph(doc,
        "Por meio deste Termo, o(a) servidor(a) abaixo identificado(a) declara ter "
        "ciência da Política de Governança de Inteligência Artificial da Câmara dos "
        "Deputados, estabelecida pela Portaria nº 227, de 23 de dezembro de 2025, "
        "que regulamenta o Ato da Mesa nº 225, de 15 de dezembro de 2025, e "
        "compromete-se a observar os princípios, diretrizes e vedações nela "
        "estabelecidos."
    )

    add_docx_section(doc, "2. IDENTIFICAÇÃO DO SERVIDOR")
    add_docx_field(doc, "Nome completo:", lines=1)
    add_docx_field(doc, "Matrícula:", lines=1)
    add_docx_field(doc, "Unidade administrativa:", lines=1)
    add_docx_field(doc, "Cargo/Função:", lines=1)

    add_docx_section(doc, "3. PRINCÍPIOS ÉTICOS (Art. 4º)")
    add_docx_paragraph(doc,
        "Declaro ciência de que a concepção, o uso, o desenvolvimento, a contratação "
        "e a implantação de sistemas de IA na Câmara dos Deputados devem observar os "
        "seguintes princípios éticos:",
        size=10
    )
    principios = [
        "I — tratamento de dados com boa fé e finalidade legítima;",
        "II — proteção do direito à privacidade e dos dados pessoais;",
        "III — transparência e publicidade responsável dos procedimentos e decisões;",
        "IV — responsabilização e prestação de contas;",
        "V — apresentação de resultados justos, isentos de vieses, inclusivos e não discriminatórios;",
        "VI — operação de acordo com os propósitos para os quais foram projetados, com dados íntegros, "
        "respeitando acessos autorizados, de maneira a possuir resiliência a falhas no funcionamento "
        "ou a incidentes de segurança;",
        "VII — primazia da decisão humana, com garantia de autonomia no uso de sistemas de IA e de "
        "supervisão contínua sobre o comportamento desses sistemas;",
        "VIII — respeito à propriedade intelectual, ao segredo industrial e aos direitos autorais."
    ]
    for p in principios:
        add_docx_paragraph(doc, p, size=10)

    add_docx_section(doc, "4. COMPROMISSOS ASSUMIDOS")
    add_docx_paragraph(doc,
        "Comprometo-me a observar as seguintes diretrizes no uso de sistemas de "
        "inteligência artificial:",
        size=10
    )

    compromissos = [
        ("4.1", "NÃO submeter dados pessoais, mesmo anonimizados, a sistemas de IA em nuvem pública "
         "sem autorização prévia e expressa do Gestor de Dados e do Encarregado de Proteção de Dados "
         "Pessoais. [Art. 8º]"),
        ("4.2", "NÃO submeter dados com restrição de acesso (sigilosos, protegidos por sigilo legal, "
         "que coloquem processos corporativos em risco, ou credenciais de acesso) para uso por "
         "sistemas de IA em nuvem pública. [Art. 19]"),
        ("4.3", "NÃO utilizar informações corporativas, como endereço de e-mail ou ponto, para criação "
         "de contas em sistemas de IA generativa que funcionem em nuvem não contratada pela Câmara "
         "dos Deputados. [Art. 9º]"),
        ("4.4", "REVISAR obrigatoriamente os resultados obtidos com o uso de IA generativa antes de "
         "torná-los públicos ou utilizá-los em processos de trabalho e decisões, sendo responsável "
         "pelos documentos que criar e publicar. [Art. 14]"),
        ("4.5", "VERIFICAR a fonte dos dados e indicá-las, com reconhecimento dos respectivos autores, "
         "em documentos produzidos a partir de sistema de IA generativa. [Art. 21]"),
        ("4.6", "INFORMAR quando um documento ou comunicação tiver sido produzido com auxílio de "
         "inteligência artificial. [Art. 12]"),
        ("4.7", "EVITAR a adoção de decisões automatizadas criadas por sistemas de IA sem revisão "
         "humana. [Art. 14, Parágrafo único]"),
        ("4.8", "COMUNICAR à Ditec quando identificar riscos ou problemas na aplicação dos princípios "
         "éticos no uso da IA. [Art. 32-IV]"),
        ("4.9", "EVITAR o uso de dados pessoais por sistemas de IA, documentando justificativa formal "
         "quando o tratamento for estritamente necessário. [Arts. 6º, 7º]"),
    ]
    for num, texto in compromissos:
        p = doc.add_paragraph()
        run_num = p.add_run(f"{num}  ")
        run_num.bold = True
        run_num.font.size = Pt(10)
        run_text = p.add_run(texto)
        run_text.font.size = Pt(10)

    add_docx_section(doc, "5. VEDAÇÕES (Art. 15)")
    add_docx_paragraph(doc,
        "Declaro ciência de que são vedados o uso e o desenvolvimento de sistemas de IA que:",
        size=10
    )
    vedacoes = [
        "I — gerem resultados discriminatórios ilícitos ou abusivos;",
        "II — criem ou reforcem vieses contra qualquer entidade representada nos dados;",
        "III — valorem traços de personalidade, características de comportamentos naturais "
        "ou de grupos de pessoas naturais para fins de avaliação de perfis naturais."
    ]
    for v in vedacoes:
        add_docx_paragraph(doc, v, size=10)

    add_docx_section(doc, "6. DECLARAÇÃO")
    add_docx_paragraph(doc,
        "Declaro que li e compreendi integralmente a Portaria nº 227/2025 e o Ato da "
        "Mesa nº 225/2025, e comprometo-me a observar todas as diretrizes, princípios "
        "e vedações neles contidos.",
        size=10
    )
    add_docx_paragraph(doc,
        "Declaro estar ciente de que sou responsável pelos documentos que criar e "
        "publicar a partir de resultados obtidos com o uso de IA generativa (Art. 14).",
        size=10, bold=True
    )

    add_signature_block(doc, [
        "Servidor(a)",
        "Chefia Imediata (Ciência)"
    ])

    add_docx_footer(doc)
    save_docx(doc, "DOC-08_Termo_Ciencia_Uso_Responsavel_IA.docx")


def create_doc09():
    """DOC-09: Template de Documentação de Uso Contínuo de IA Generativa"""
    print("DOC-09: Template de Documentação de Uso Contínuo de IA Generativa...")
    wb = new_workbook()
    ws = add_sheet(wb, "Uso Contínuo IA Generativa")
    NC = 6
    set_col_widths(ws, [5, 30, 22, 22, 22, 22])

    r = 1
    write_title_row(ws, r, "TEMPLATE DE DOCUMENTAÇÃO DE USO CONTÍNUO DE IA GENERATIVA", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025 — Arts. 31-II, 31-III", NC)

    # Referência normativa
    r += 2
    refs = [
        ('Art. 31-II', 'Cabe ao Gestor de Negócio submeter à análise da Ditec documentação que '
                        'apresente como pretende utilizar a IA generativa de maneira contínua em '
                        'seus processos de trabalho, caso esse uso não esteja contemplado em projeto.'),
        ('Art. 31-III', 'Cabe ao Gestor de Negócio supervisionar processos de trabalho que utilizem '
                         'de maneira contínua a IA generativa, atendendo aos padrões de documentação '
                         'e comunicação estabelecidos pela Ditec.'),
    ]
    for art, texto in refs:
        r += 1
        ws.cell(row=r, column=1, value=art).font = font_label()
        ws.cell(row=r, column=1).alignment = ALIGN_CENTER
        ws.cell(row=r, column=1).border = THIN_BORDER
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=NC)
        ws.cell(row=r, column=2, value=texto).font = Font(name='Arial', size=9, italic=True, color=DARK_BLUE)
        ws.cell(row=r, column=2).alignment = ALIGN_LEFT
        ws.cell(row=r, column=2).border = THIN_BORDER
        for c in range(3, NC + 1):
            ws.cell(row=r, column=c).border = THIN_BORDER
        ws.row_dimensions[r].height = 40

    # Seção 1: Identificação
    r += 2
    write_section_header(ws, r, "1. IDENTIFICAÇÃO DA UNIDADE E PROCESSO", NC)
    r += 1
    write_form_field(ws, r, "Unidade administrativa", 1, 2, NC, is_required=True)
    r += 1
    write_form_field(ws, r, "Gestor de Negócio", 1, 2, 4, is_required=True)
    write_form_field(ws, r, "Data", 5, 6, NC)
    r += 1
    write_form_field(ws, r, "Processo de trabalho", 1, 2, NC, is_required=True)
    ws.row_dimensions[r].height = 40
    r += 1
    write_form_field(ws, r, "Descrição do uso de IA generativa no processo", 1, 2, NC, is_required=True)
    ws.row_dimensions[r].height = 60

    # Seção 2: Ferramenta
    r += 2
    write_section_header(ws, r, "2. FERRAMENTA DE IA UTILIZADA", NC)
    r += 1
    write_form_field(ws, r, "Nome da ferramenta", 1, 2, NC, is_required=True)
    r += 1
    write_form_field(ws, r, "Tipo", 1, 2, 3)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Chatbot/Assistente", "Geração de texto", "Geração de código",
                  "Análise de dados", "Geração de imagens", "Outro"])
    write_form_field(ws, r, "Contratada pela Câmara?", 4, 5, NC)
    add_dropdown(ws, ws.cell(row=r, column=5), ["Sim", "Não"])
    r += 1
    write_form_field(ws, r, "Ambiente", 1, 2, 3, ref_artigo="Arts. 2º XII-XIII")
    add_dropdown(ws, ws.cell(row=r, column=2), ["Infra própria", "Nuvem privada", "Nuvem pública"])
    write_form_field(ws, r, "Frequência de uso", 4, 5, NC)
    add_dropdown(ws, ws.cell(row=r, column=5), ["Diário", "Semanal", "Mensal", "Eventual"])

    # Seção 3: Dados
    r += 2
    write_section_header(ws, r, "3. DADOS ENVOLVIDOS", NC)
    r += 1
    write_form_field(ws, r, "Tipo de dados enviados à ferramenta", 1, 2, NC, is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Apenas dados públicos", "Dados internos não restritos",
                  "Dados pessoais — com autorização", "Dados restritos — VEDADO em nuvem pública"])
    r += 1
    write_form_field(ws, r, "Descrição dos dados", 1, 2, NC)
    ws.row_dimensions[r].height = 40
    r += 1
    write_form_field(ws, r, "Gestor de Dados responsável", 1, 2, NC)
    r += 1
    write_form_field(ws, r, "Autorização de acesso obtida?", 1, 2, 3, ref_artigo="Art. 31-I")
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim", "Não — pendente", "N/A — sem dados corporativos"])

    # Seção 4: Riscos
    r += 2
    write_section_header(ws, r, "4. RISCOS IDENTIFICADOS E MEDIDAS DE MITIGAÇÃO", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Risco Identificado", "Princípio Ético\nAfetado [Art. 4º]",
                               "Nível", "Medida de Mitigação", "Status"])
    for i in range(1, 6):
        r += 1
        fills = [None] + [fill_yellow()] * 5
        write_data_row(ws, r, [i, "", "", "", "", ""], fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Crítico", "Alto", "Médio", "Baixo"])
        add_dropdown(ws, ws.cell(row=r, column=6), ["Implementado", "Em andamento", "Pendente"])

    # Seção 5: Supervisão
    r += 2
    write_section_header(ws, r, "5. SUPERVISÃO  [Art. 31-III]", NC)
    r += 1
    write_form_field(ws, r, "Procedimento de revisão de outputs", 1, 2, NC, ref_artigo="Art. 14")
    ws.row_dimensions[r].height = 40
    r += 1
    write_form_field(ws, r, "Frequência de supervisão", 1, 2, 3)
    add_dropdown(ws, ws.cell(row=r, column=2), ["Contínua", "Semanal", "Mensal", "Trimestral"])
    write_form_field(ws, r, "Indicadores monitorados", 4, 5, NC)

    # Seção 6: Aprovação Ditec
    r += 2
    write_section_header(ws, r, "6. APROVAÇÃO DA DITEC  [Art. 31-II]", NC)
    r += 1
    write_form_field(ws, r, "Decisão da Ditec", 1, 2, NC, is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Aprovado", "Aprovado com condições", "Não aprovado — ajustes necessários",
                  "Não aprovado — vedação aplicável"])
    r += 1
    write_form_field(ws, r, "Condições / Observações", 1, 2, NC)
    ws.row_dimensions[r].height = 50
    r += 1
    write_form_field(ws, r, "Responsável Ditec — Nome", 1, 2, 4)
    write_form_field(ws, r, "Data", 5, 6, NC)

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-09_Template_Documentacao_Uso_Continuo_IA_Generativa.xlsx")


def create_doc13():
    """DOC-13: Template de Parecer do CETIA (.docx)"""
    print("DOC-13: Template de Parecer do CETIA...")
    doc = new_document(
        "PARECER DO COMITÊ DE ÉTICA NO USO DA INTELIGÊNCIA ARTIFICIAL (CETIA)",
        "Portaria 227/2025, Arts. 23-24, 34"
    )

    # Cabeçalho do parecer
    add_docx_section(doc, "DADOS DO PARECER")
    add_docx_field(doc, "Parecer CETIA nº:", lines=1)
    add_docx_field(doc, "Data:", lines=1)
    add_docx_field(doc, "Tipo:", lines=1)
    add_docx_paragraph(doc,
        "( ) Avaliação de nova demanda de sistema de IA [Art. 34-I]\n"
        "( ) Avaliação de sistema em desenvolvimento/operação [Art. 34-II]\n"
        "( ) Relatório executivo periódico [Art. 34-IV]",
        size=10
    )

    add_docx_section(doc, "1. PROJETO / DEMANDA AVALIADA")
    add_docx_field(doc, "Nome do projeto/sistema de IA:")
    add_docx_field(doc, "Unidade demandante:")
    add_docx_field(doc, "Responsável técnico (Ditec):")
    add_docx_field(doc, "Descrição resumida:")

    add_docx_section(doc, "2. RESUMO DA AVALIAÇÃO DE RISCOS DA DITEC [Art. 24, caput]")
    add_docx_paragraph(doc,
        "A Ditec realizou avaliação de riscos quanto à violação dos princípios éticos "
        "desta Portaria, conforme Art. 24, cujo resumo segue:",
        size=10
    )
    add_docx_field(doc, "Classificação de risco atribuída pela Ditec:")
    add_docx_field(doc, "Principais riscos identificados:", lines=3)
    add_docx_field(doc, "Medidas de mitigação propostas pela Ditec:", lines=3)

    add_docx_section(doc, "3. ANÁLISE POR PRINCÍPIO ÉTICO [Art. 4º]")

    principios_analise = [
        ("I", "Tratamento de dados com boa fé e finalidade legítima"),
        ("II", "Proteção do direito à privacidade e dos dados pessoais"),
        ("III", "Transparência e publicidade responsável"),
        ("IV", "Responsabilização e prestação de contas"),
        ("V", "Resultados justos, isentos de vieses, não discriminatórios"),
        ("VI", "Operação conforme propósitos, resiliência a falhas"),
        ("VII", "Primazia da decisão humana, supervisão contínua"),
        ("VIII", "Respeito à propriedade intelectual e direitos autorais"),
    ]
    headers_p = ["Inciso", "Princípio", "Análise do CETIA", "Risco"]
    rows_p = [[inc, nome, "", ""] for inc, nome in principios_analise]
    add_docx_table(doc, headers_p, rows_p)

    add_docx_section(doc, "4. VERIFICAÇÃO DE VEDAÇÕES [Art. 15]")
    add_docx_paragraph(doc,
        "O CETIA verificou se a demanda envolve:",
        size=10
    )
    vedacoes_cetia = [
        "( ) Geração de resultados discriminatórios ilícitos ou abusivos [Art. 15-I]",
        "( ) Criação ou reforço de vieses contra entidades representadas nos dados [Art. 15-II]",
        "( ) Valoração de traços de personalidade ou perfilamento [Art. 15-III]",
    ]
    for v in vedacoes_cetia:
        add_docx_paragraph(doc, v, size=10)
    add_docx_field(doc, "Resultado da verificação de vedações:", lines=2)

    add_docx_section(doc, "5. CLASSIFICAÇÃO DE RISCO PELO CETIA")
    add_docx_paragraph(doc,
        "Com base na análise realizada, o CETIA classifica o risco da demanda como:",
        size=10
    )
    add_docx_paragraph(doc,
        "( ) BAIXO — aprovação simplificada\n"
        "( ) MÉDIO — aprovação com condições padrão\n"
        "( ) ALTO — REJEIÇÃO AUTOMÁTICA (Art. 24, §2º)\n"
        "       Justificativas serão comunicadas à Ditec, ao CDTI e ao CGE.",
        size=10
    )
    add_docx_paragraph(doc,
        'Art. 24, §2º: "Caso o parecer do CETIA indique alto risco para a Câmara dos '
        'Deputados ou para os cidadãos, a demanda será rejeitada, sendo as justificativas '
        'comunicadas à Ditec, ao Comitê Diretivo de TIC (CDTI) e ao Comitê de Gestão '
        'Estratégica (CGE)."',
        italic=True, size=9
    )

    add_docx_section(doc, "6. CONDIÇÕES DE APROVAÇÃO [Art. 24, §1º]")
    add_docx_paragraph(doc,
        'Art. 24, §1º: "A análise do CETIA indicará se há condições para a demanda '
        'obter aprovação, observados o modelo de governança de TIC, assim como o nível '
        'de documentação e de monitoramento necessários."',
        italic=True, size=9
    )
    add_docx_field(doc, "Condições para aprovação:", lines=3)

    add_docx_section(doc, "7. NÍVEL DE DOCUMENTAÇÃO EXIGIDO [Art. 24, §1º]")
    add_docx_paragraph(doc,
        "( ) Documentação básica (formulário de uso contínuo)\n"
        "( ) Documentação intermediária (mapeamento de dados + avaliação de riscos)\n"
        "( ) Documentação completa (todos os artefatos do ciclo de vida)",
        size=10
    )

    add_docx_section(doc, "8. NÍVEL DE MONITORAMENTO EXIGIDO [Art. 24, §1º]")
    add_docx_paragraph(doc,
        "( ) Monitoramento padrão (supervisão contínua compartilhada — Art. 27)\n"
        "( ) Monitoramento reforçado (relatórios mensais + testes éticos trimestrais)\n"
        "( ) Monitoramento intensivo (relatórios quinzenais + testes éticos mensais)",
        size=10
    )

    add_docx_section(doc, "9. CONSULTA AO CGSIC [Art. 24, §3º]")
    add_docx_paragraph(doc,
        'Art. 24, §3º: "Caso envolvam aspectos de segurança da informação e cibernética, '
        'antes de emitir seu parecer, o CETIA deve consultar o CGSIC."',
        italic=True, size=9
    )
    add_docx_paragraph(doc,
        "( ) Consulta ao CGSIC realizada — Parecer anexo\n"
        "( ) Consulta ao CGSIC não necessária",
        size=10
    )
    add_docx_field(doc, "Resumo do parecer do CGSIC (se aplicável):", lines=2)

    add_docx_section(doc, "10. CONCLUSÃO")
    add_docx_paragraph(doc,
        "( ) APROVADO — com as condições acima estabelecidas\n"
        "( ) APROVADO COM RESSALVAS — requer adequações antes da implantação\n"
        "( ) REJEITADO — alto risco (Art. 24§2º) — comunicar Ditec, CDTI e CGE\n"
        "( ) RETORNAR À DITEC — informações insuficientes para análise",
        size=10
    )
    add_docx_field(doc, "Justificativa:", lines=3)

    add_docx_section(doc, "11. COMUNICAÇÃO [Art. 34-III]")
    add_docx_paragraph(doc,
        'Art. 34-III: "comunicar os pareceres e recomendações emitidos sobre os riscos '
        'de IA avaliados à Ditec, ao CDTI e ao CGE"',
        italic=True, size=9
    )
    add_docx_paragraph(doc,
        "Comunicar a:\n"
        "( ) Ditec\n"
        "( ) CDTI\n"
        "( ) CGE",
        size=10
    )

    add_docx_section(doc, "12. ASSINATURAS — MEMBROS DO CETIA [Art. 23]")

    membros = [
        "Presidente — Assessoria de Projetos e Gestão (Aproge) [Art. 23-I]",
        "Representante — Secretaria-Geral da Mesa [Art. 23-II]",
        "Representante — Advocacia da Câmara dos Deputados [Art. 23-III]",
        "Representante — Diretoria de Inovação e Tecnologia da Informação (Ditec) [Art. 23-IV]",
        "Representante — Diretoria de Gestão de Pessoas / Coord. Resp. Social [Art. 23-V]",
        "Representante — Centro de Documentação e Informação (Cedi) [Art. 23-VI]",
        "Encarregado de Proteção de Dados Pessoais [Art. 23, caput]",
    ]
    add_signature_block(doc, membros)

    add_docx_footer(doc)
    save_docx(doc, "DOC-13_Template_Parecer_CETIA.docx")


def create_doc14():
    """DOC-14: Template de Relatório de Supervisão Periódica de IA"""
    print("DOC-14: Template de Relatório de Supervisão Periódica de IA...")
    wb = new_workbook()
    ws = add_sheet(wb, "Supervisão Periódica IA")
    NC = 6
    set_col_widths(ws, [5, 32, 20, 18, 22, 22])

    r = 1
    write_title_row(ws, r, "RELATÓRIO DE SUPERVISÃO PERIÓDICA DE SISTEMA DE IA", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025 — Arts. 27, 31-III, 31-VI", NC)

    # Seção 1: Identificação
    r += 2
    write_section_header(ws, r, "1. IDENTIFICAÇÃO", NC)
    r += 1
    write_form_field(ws, r, "Sistema de IA", 1, 2, NC, is_required=True)
    r += 1
    write_form_field(ws, r, "Período de supervisão", 1, 2, 4, is_required=True)
    write_form_field(ws, r, "Relatório nº", 5, 6, NC)
    r += 1
    write_form_field(ws, r, "Gestor de Negócio", 1, 2, NC)
    r += 1
    write_form_field(ws, r, "Gestor de Dados", 1, 2, NC)
    r += 1
    write_form_field(ws, r, "Responsável Ditec", 1, 2, NC)

    # Seção 2: Indicadores de Performance
    r += 2
    write_section_header(ws, r, "2. INDICADORES DE PERFORMANCE", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Indicador", "Meta", "Resultado\nPeríodo", "Tendência", "Observações"])
    indicadores = [
        "Acurácia / Qualidade dos resultados",
        "Taxa de alucinações detectadas [Art. 26§4º]",
        "Taxa de vieses identificados [Art. 26§4º]",
        "Tempo de resposta / Disponibilidade",
        "Volume de uso (requisições/documentos)",
    ]
    for i, ind in enumerate(indicadores, 1):
        r += 1
        fills = [None, None, fill_yellow(), fill_yellow(), fill_yellow(), fill_yellow()]
        write_data_row(ws, r, [i, ind, "", "", "", ""], fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=5), ["Melhora", "Estável", "Piora"])
    # Linhas extras
    for i in range(len(indicadores) + 1, len(indicadores) + 4):
        r += 1
        fills = [None] + [fill_yellow()] * 5
        write_data_row(ws, r, [i, "", "", "", "", ""], fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=5), ["Melhora", "Estável", "Piora"])

    # Seção 3: Qualidade de Dados
    r += 2
    write_section_header(ws, r, "3. QUALIDADE DE DADOS  [Arts. 29-VII, 30-III, 31-V]", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Aspecto", "Avaliação", "Ação Necessária", "Responsável", "Prazo"])
    aspectos_dados = [
        "Integridade dos dados de entrada",
        "Atualização dos dados de treinamento/contexto",
        "Qualidade dos dados RAG [Art. 25-III-b]",
        "Conformidade com classificação de sigilo [Art. 17]",
        "Dados pessoais — conformidade LGPD [Art. 7º]",
    ]
    for i, asp in enumerate(aspectos_dados, 1):
        r += 1
        fills = [None, None, fill_yellow(), fill_yellow(), fill_yellow(), fill_yellow()]
        write_data_row(ws, r, [i, asp, "", "", "", ""], fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=3), ["Adequado", "Requer atenção", "Crítico", "N/A"])

    # Seção 4: Conformidade com Princípios Éticos
    r += 2
    write_section_header(ws, r, "4. CONFORMIDADE COM PRINCÍPIOS ÉTICOS  [Art. 27§1º]", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Princípio Ético (Art. 4º)", "Status", "Observações\ndo Período", "Ação Requerida", "Responsável"])
    principios_sup = [
        ("I", "Boa fé e finalidade legítima"),
        ("II", "Privacidade e dados pessoais"),
        ("III", "Transparência e publicidade"),
        ("IV", "Responsabilização e prestação de contas"),
        ("V", "Resultados justos e não discriminatórios"),
        ("VI", "Resiliência a falhas e incidentes"),
        ("VII", "Primazia da decisão humana"),
        ("VIII", "Propriedade intelectual"),
    ]
    for i, (inc, princ) in enumerate(principios_sup, 1):
        r += 1
        fills = [None, None, fill_yellow(), fill_yellow(), fill_yellow(), fill_yellow()]
        write_data_row(ws, r, [i, f"{inc} — {princ}", "", "", "", ""], fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=3), ["Conforme", "Atenção", "Não conforme", "N/A"])

    # Seção 5: Incidentes
    r += 2
    write_section_header(ws, r, "5. INCIDENTES NO PERÍODO", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Descrição do Incidente", "Data", "Severidade", "Ação Tomada", "Status"])
    for i in range(1, 6):
        r += 1
        fills = [None] + [fill_yellow()] * 5
        write_data_row(ws, r, [i, "", "", "", "", ""], fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Crítico", "Alto", "Médio", "Baixo"])
        add_dropdown(ws, ws.cell(row=r, column=6), ["Resolvido", "Em andamento", "Pendente"])

    # Seção 6: Necessidades Identificadas (Art. 27§2º)
    r += 2
    write_section_header(ws, r, "6. NECESSIDADES IDENTIFICADAS  [Art. 27, §2º]", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Necessidade (conforme Art. 27§2º)", "Identificada?",
                               "Descrição", "Ação Proposta", "Prazo"])
    necessidades = [
        ("I", "Ajustes em dados"),
        ("II", "Ajustes em outros sistemas que geram dados para o sistema de IA"),
        ("III", "Novo treinamento do sistema de IA"),
        ("IV", "Ajustes nas regras de negócio do sistema de IA"),
        ("V", "Suspensão ou exclusão do sistema de IA do portfólio"),
    ]
    for i, (inc, nec) in enumerate(necessidades, 1):
        r += 1
        fills = [None, None, fill_yellow(), fill_yellow(), fill_yellow(), fill_yellow()]
        write_data_row(ws, r, [i, f"{inc} — {nec}", "", "", "", ""], fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=3), ["Sim", "Não"])
        ws.row_dimensions[r].height = 35

    # Seção 7: Monitoramento de Segurança
    r += 2
    write_section_header(ws, r, "7. MONITORAMENTO DE SEGURANÇA  [Art. 27, §3º]", NC)
    r += 1
    write_form_field(ws, r, "Ataques detectados no período?", 1, 2, 3)
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim", "Não"])
    write_form_field(ws, r, "Integridade comprometida?", 4, 5, NC)
    add_dropdown(ws, ws.cell(row=r, column=5), ["Sim", "Não"])
    r += 1
    write_form_field(ws, r, "Privacidade comprometida?", 1, 2, 3)
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim", "Não"])
    r += 1
    write_form_field(ws, r, "Detalhamento (se aplicável)", 1, 2, NC)
    ws.row_dimensions[r].height = 50

    # Seção 8: Recomendações
    r += 2
    write_section_header(ws, r, "8. RECOMENDAÇÕES", NC)
    r += 1
    write_form_field(ws, r, "Recomendações para o próximo período", 1, 2, NC)
    ws.row_dimensions[r].height = 80

    # Seção 9: Assinaturas
    r += 2
    write_section_header(ws, r, "9. ASSINATURAS", NC)
    assinaturas = [
        ("Gestor de Negócio [Art. 31-VI]", 1, 3),
        ("Gestor de Dados [Art. 30-IV]", 4, NC),
    ]
    r += 1
    for nome, c_start, c_end in assinaturas:
        ws.merge_cells(start_row=r, start_column=c_start, end_row=r, end_column=c_end)
        cell = ws.cell(row=r, column=c_start, value=nome)
        cell.font = font_label()
        cell.alignment = ALIGN_CENTER
        cell.border = THIN_BORDER
        for c in range(c_start + 1, c_end + 1):
            ws.cell(row=r, column=c).border = THIN_BORDER
    r += 1
    for nome, c_start, c_end in assinaturas:
        ws.merge_cells(start_row=r, start_column=c_start, end_row=r, end_column=c_end)
        cell = ws.cell(row=r, column=c_start)
        cell.fill = fill_yellow()
        cell.border = THIN_BORDER
        for c in range(c_start + 1, c_end + 1):
            ws.cell(row=r, column=c).border = THIN_BORDER
            ws.cell(row=r, column=c).fill = fill_yellow()
    ws.row_dimensions[r].height = 40

    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=NC)
    cell = ws.cell(row=r, column=1, value="Responsável Ditec [Art. 29-VIII]")
    cell.font = font_label()
    cell.alignment = ALIGN_CENTER
    cell.border = THIN_BORDER
    for c in range(2, NC + 1):
        ws.cell(row=r, column=c).border = THIN_BORDER
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=NC)
    cell = ws.cell(row=r, column=1)
    cell.fill = fill_yellow()
    cell.border = THIN_BORDER
    for c in range(2, NC + 1):
        ws.cell(row=r, column=c).border = THIN_BORDER
        ws.cell(row=r, column=c).fill = fill_yellow()
    ws.row_dimensions[r].height = 40

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-14_Template_Relatorio_Supervisao_Periodica_IA.xlsx")
