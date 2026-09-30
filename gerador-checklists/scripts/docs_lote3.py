# -*- coding: utf-8 -*-
"""
docs_lote3.py — Checklists (DOC-04, DOC-07, DOC-10, DOC-11)
"""
from docs_operacionais_helpers import *


def create_doc04():
    """DOC-04: Checklist de Conformidade com 3 Políticas (Dados, SI, PDP)"""
    print("DOC-04: Checklist de Conformidade com 3 Políticas...")
    wb = new_workbook()
    ws = add_sheet(wb, "Conformidade 3 Políticas")
    NC = 6
    set_col_widths(ws, [5, 50, 16, 16, 22, 22])

    r = 1
    write_title_row(ws, r, "CHECKLIST DE CONFORMIDADE COM 3 POLÍTICAS", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025, Art. 13, Parágrafo único", NC)

    # Referência
    r += 2
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=NC)
    cell = ws.cell(row=r, column=1,
                   value='Art. 13, Parágrafo único: "Os processos referidos no caput devem considerar '
                         'a Política de Governança de Dados, a Política de Segurança da Informação e '
                         'Cibernética e a Política de Proteção de Dados Pessoais."')
    cell.font = Font(name='Arial', size=9, italic=True, color=DARK_BLUE)
    cell.alignment = ALIGN_LEFT
    cell.border = THIN_BORDER
    for c in range(2, NC + 1):
        ws.cell(row=r, column=c).border = THIN_BORDER

    # Identificação
    r += 2
    write_section_header(ws, r, "IDENTIFICAÇÃO DO PROJETO / PROCESSO", NC)
    r += 1
    write_form_field(ws, r, "Projeto/processo de IA", 1, 2, 4, is_required=True)
    write_form_field(ws, r, "Data", 5, 6, NC)
    r += 1
    write_form_field(ws, r, "Avaliador", 1, 2, 4)
    write_form_field(ws, r, "Unidade", 5, 6, NC)

    # Headers
    checklist_headers = ["#", "Item de Verificação", "Referência", "Status", "Evidência", "Observações"]

    # === SEÇÃO 1: PG-Dados (Portaria 226/2025) ===
    r += 2
    write_section_header(ws, r, "SEÇÃO 1: POLÍTICA DE GOVERNANÇA DE DADOS (Portaria 226/2025)", NC)
    r += 1
    write_col_headers(ws, r, checklist_headers)

    itens_pgdados = [
        ("Gestor de dados formalmente designado para os dados do projeto?", "Port. 226, Art. 18"),
        ("Dados registrados no Catálogo de Metadados?", "Port. 226, Art. 17"),
        ("Curador de dados designado para as bases utilizadas?", "Port. 226, Art. 22§1º-I"),
        ("Bases de dados em conformidade com normas de modelagem?", "Port. 226, Art. 22§1º-IV"),
        ("Finalidade de tratamento definida conforme processo de trabalho?", "Port. 226, Art. 18-VIII"),
        ("Regras de acesso definidas conforme critérios de segurança?", "Port. 226, Art. 18-XI"),
        ("Prazo de retenção dos dados definido?", "Port. 226, Art. 18-IX"),
        ("Qualidade dos dados avaliada (precisão, integridade, consistência)?", "Port. 226, Art. 3º-XIX"),
    ]
    for i, (item, ref) in enumerate(itens_pgdados, 1):
        r += 1
        write_checklist_row(ws, r, i, item, ref, NC)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Conforme", "Não conforme", "Parcial", "N/A"])

    # === SEÇÃO 2: POSIC / Segurança da Informação e Cibernética ===
    r += 2
    write_section_header(ws, r, "SEÇÃO 2: POLÍTICA DE SEGURANÇA DA INFORMAÇÃO E CIBERNÉTICA (POSIC)", NC)
    r += 1
    write_col_headers(ws, r, checklist_headers)

    itens_posic = [
        ("Classificação de sigilo dos dados definida?", "Port. 227, Art. 17"),
        ("Testes de robustez realizados (resiliência a falhas e vulnerabilidades)?", "Port. 227, Art. 16"),
        ("Dados restritos tratados apenas em infra própria ou nuvem privada?", "Port. 227, Art. 19"),
        ("Monitoramento contínuo contra ataques de segurança implementado?", "Port. 227, Art. 27§3º"),
        ("Riscos de incidentes de segurança identificados?", "Port. 227, Art. 26§3º"),
        ("Plano de testes para comportamentos inadequados definido?", "Port. 227, Art. 26§3º"),
        ("CGSIC consultado (se aspectos de segurança envolvidos)?", "Port. 227, Art. 24§3º"),
        ("Medidas de resiliência a incidentes definidas?", "Port. 227, Art. 29-V"),
    ]
    for i, (item, ref) in enumerate(itens_posic, 1):
        r += 1
        write_checklist_row(ws, r, i, item, ref, NC)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Conforme", "Não conforme", "Parcial", "N/A"])

    # === SEÇÃO 3: PDP / LGPD (Ato 152/2020) ===
    r += 2
    write_section_header(ws, r, "SEÇÃO 3: POLÍTICA DE PROTEÇÃO DE DADOS PESSOAIS (Ato 152/2020 + LGPD)", NC)
    r += 1
    write_col_headers(ws, r, checklist_headers)

    itens_pdp = [
        ("Uso de dados pessoais é evitado? Justificativa documentada se necessário?", "Port. 227, Art. 6º"),
        ("Autorização formal do Gestor de Dados e Encarregado obtida?", "Port. 227, Art. 7º§1º"),
        ("Base legal LGPD identificada para o tratamento?", "Ato 152, Art. 2º"),
        ("ROPA elaborado (se dados pessoais)?", "Port. 226, Art. 14-IV"),
        ("RIPD elaborado (se tratamento de alto risco)?", "Port. 226, Art. 14-V"),
        ("Dados pessoais anonimizados quando necessário?", "Port. 227, Art. 7º§2º"),
        ("Vedação de dados pessoais em nuvem pública sem autorização verificada?", "Port. 227, Art. 8º"),
        ("Encarregado comunicado sobre tratamento de dados pessoais?", "Ato 152, Art. 10§3º"),
        ("GT-LGPD aprovou ROPA/RIPD?", "Port. 226, Art. 15"),
    ]
    for i, (item, ref) in enumerate(itens_pdp, 1):
        r += 1
        write_checklist_row(ws, r, i, item, ref, NC)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Conforme", "Não conforme", "Parcial", "N/A"])

    # Resultado consolidado
    r += 2
    write_section_header(ws, r, "RESULTADO CONSOLIDADO", NC)
    r += 1
    write_form_field(ws, r, "Resultado geral", 1, 2, 3, is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Conforme — prosseguir", "Parcialmente conforme — ajustes necessários",
                  "Não conforme — não prosseguir"])
    write_form_field(ws, r, "Data", 4, 5, NC)
    r += 1
    write_form_field(ws, r, "Ações corretivas necessárias", 1, 2, NC)
    ws.row_dimensions[r].height = 50
    r += 1
    write_form_field(ws, r, "Avaliador — Nome e Assinatura", 1, 2, NC)

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-04_Checklist_Conformidade_3_Politicas.xlsx")


def create_doc07():
    """DOC-07: Checklist de Artefatos por Fase do Ciclo de Vida"""
    print("DOC-07: Checklist de Artefatos por Fase do Ciclo de Vida...")
    wb = new_workbook()
    ws = add_sheet(wb, "Artefatos Ciclo de Vida")
    NC = 6
    set_col_widths(ws, [5, 42, 18, 16, 22, 22])

    r = 1
    write_title_row(ws, r, "CHECKLIST DE ARTEFATOS POR FASE DO CICLO DE VIDA DE IA", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025 — Arts. 2º-IV, 11, 22-Pú, 26", NC)

    # Identificação
    r += 2
    write_section_header(ws, r, "IDENTIFICAÇÃO", NC)
    r += 1
    write_form_field(ws, r, "Sistema/Projeto de IA", 1, 2, 4, is_required=True)
    write_form_field(ws, r, "Data", 5, 6, NC)
    r += 1
    write_form_field(ws, r, "Responsável (Ditec)", 1, 2, 4, ref_artigo="Art. 22-Pú")

    checklist_headers = ["#", "Artefato Obrigatório", "Responsável", "Status", "Evidência/Localização", "Observações"]

    # Fases do ciclo de vida (Art. 2º, IV)
    fases = {
        "FASE 1: PLANEJAMENTO": [
            ("Avaliação de riscos éticos submetida ao CETIA", "Ditec", "Art. 24"),
            ("Parecer do CETIA obtido", "CETIA", "Art. 24§1º"),
            ("Consulta ao CGSIC (se segurança envolvida)", "CETIA", "Art. 24§3º"),
            ("Matriz RACI do projeto", "Gestor de Negócio", "Art. 13"),
            ("Checklist de conformidade com 3 políticas", "Gestor de Negócio", "Art. 13-Pú"),
            ("Mapeamento e classificação de dados", "Gestor de Dados", "Arts. 6º-8º"),
            ("Autorização de acesso a dados obtida", "Gestor de Dados", "Art. 7º§1º, 18"),
            ("Definição de requisitos de negócio", "Gestor de Negócio", "Art. 31-VII"),
        ],
        "FASE 2: DESENHO E PROTOTIPAÇÃO": [
            ("Arquitetura do sistema documentada", "Ditec", "Art. 29-I"),
            ("Especificação de ambiente (nuvem/infra)", "Ditec", "Arts. 2º XII-XIII"),
            ("Especificação de medidas de segurança", "Ditec", "Art. 16"),
            ("Plano de testes de robustez", "Ditec", "Art. 16, 26§3º"),
        ],
        "FASE 3: COLETA E PREPARAÇÃO DE DADOS": [
            ("Autorização formal de cada Gestor de Dados", "Gestor de Dados", "Art. 18"),
            ("Verificação de propriedade intelectual dos datasets", "Ditec", "Art. 20"),
            ("Anonimização realizada (se dados pessoais)", "Ditec", "Art. 7º§2º"),
            ("Dados restritos excluídos de nuvem pública", "Ditec", "Art. 19"),
            ("Classificação de sigilo aplicada", "Gestor de Dados", "Art. 17"),
        ],
        "FASE 4: MODELAGEM E TREINAMENTO": [
            ("Dados de treinamento documentados e recuperáveis", "Ditec", "Art. 25-II"),
            ("Dados externos documentados", "Ditec", "Art. 25-III-a"),
            ("Medidas de controle de vieses implementadas", "Ditec", "Art. 26§4º"),
            ("Atuação conjunta negócio-Ditec documentada", "Gerente de Projeto", "Art. 26§1º"),
        ],
        "FASE 5: TESTE E AVALIAÇÃO": [
            ("Testes de robustez executados", "Ditec", "Art. 16"),
            ("Testes de vieses e alucinações executados", "Ditec", "Art. 26§4º"),
            ("Testes de comportamentos inadequados executados", "Ditec", "Art. 26§3º"),
            ("Verificação de vedações (Art. 15) executada", "CETIA", "Art. 15"),
            ("Testes de resultados discriminatórios executados", "Ditec", "Art. 15"),
            ("Verificação resultados-dados", "Ditec", "Art. 25-I"),
        ],
        "FASE 6: IMPLANTAÇÃO": [
            ("Documentação de uso entregue ao Gestor de Negócio", "Ditec", "Art. 31-II"),
            ("Aviso de interação com agente de IA implementado", "Ditec", "Art. 12"),
            ("Plano de supervisão contínua definido", "Ditec", "Art. 27"),
            ("Comunicação ao CDTI e CGE", "Ditec", "Art. 24§4º"),
        ],
        "FASE 7: MONITORAMENTO E FEEDBACK": [
            ("Supervisão contínua compartilhada em execução", "Ditec + G. Negócio + G. Dados", "Art. 27"),
            ("Monitoramento contra ataques de segurança ativo", "Ditec", "Art. 27§3º"),
            ("Testes periódicos de riscos éticos realizados", "Ditec", "Art. 27§1º"),
            ("Relatório de supervisão periódica elaborado", "Ditec", "Art. 27§2º"),
            ("Necessidades de ajustes/retreinamento/suspensão avaliadas", "Ditec", "Art. 27§2º"),
            ("Dados RAG armazenados e documentados", "Ditec", "Art. 25-III-b"),
        ],
        "FASE 8: DESATIVAÇÃO": [
            ("Procedimento de remoção do portfólio executado", "Ditec", "Art. 26"),
            ("Dados retidos conforme política de retenção", "Gestor de Dados", "Art. 26§2º"),
            ("Comunicação às partes interessadas", "Ditec", "Art. 34-III"),
            ("Registro de lições aprendidas", "Gerente de Projeto", "Art. 22"),
        ],
    }

    for fase_nome, artefatos in fases.items():
        r += 2
        write_section_header(ws, r, fase_nome, NC)
        r += 1
        write_col_headers(ws, r, checklist_headers)
        for i, (artefato, responsavel, ref) in enumerate(artefatos, 1):
            r += 1
            ws.cell(row=r, column=1, value=i).font = font_normal()
            ws.cell(row=r, column=1).alignment = ALIGN_CENTER
            ws.cell(row=r, column=2, value=artefato).font = font_normal()
            ws.cell(row=r, column=2).alignment = ALIGN_LEFT
            ws.cell(row=r, column=3, value=responsavel).font = font_normal()
            ws.cell(row=r, column=3).alignment = ALIGN_CENTER
            ws.cell(row=r, column=4).fill = fill_yellow()
            ws.cell(row=r, column=5).fill = fill_yellow()
            ws.cell(row=r, column=6).fill = fill_yellow()
            for c in range(1, NC + 1):
                ws.cell(row=r, column=c).border = THIN_BORDER
            # Referência em tooltip via comment? Colocar na obs
            ws.cell(row=r, column=6, value=ref).font = font_small()
            add_dropdown(ws, ws.cell(row=r, column=4),
                         ["Concluído", "Em andamento", "Pendente", "N/A"])
            ws.row_dimensions[r].height = 28

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-07_Checklist_Artefatos_Ciclo_Vida_IA.xlsx")


def create_doc10():
    """DOC-10: Checklist de Verificação de Fontes e Propriedade Intelectual"""
    print("DOC-10: Checklist de Verificação de Fontes e PI...")
    wb = new_workbook()
    ws = add_sheet(wb, "Fontes e PI")
    NC = 6
    set_col_widths(ws, [5, 48, 16, 16, 22, 22])

    r = 1
    write_title_row(ws, r, "CHECKLIST DE VERIFICAÇÃO DE FONTES E PROPRIEDADE INTELECTUAL", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025 — Arts. 20, 21", NC)

    # Referência normativa
    r += 2
    refs = [
        ('Art. 20', 'O uso e o desenvolvimento de sistemas de IA devem respeitar a propriedade intelectual '
                     'de conteúdos representados nos dados que utilizam.'),
        ('Art. 21', 'O usuário deve verificar a fonte dos dados e indicá-las, com reconhecimento dos seus '
                     'respectivos autores, em documentos produzidos a partir de sistema de IA generativa.'),
        ('Art. 21-Pú', 'O disposto no caput também se aplica a pesquisas desenvolvidas pela Câmara dos '
                        'Deputados em colaboração com outros órgãos.'),
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

    # Identificação
    r += 2
    write_section_header(ws, r, "IDENTIFICAÇÃO", NC)
    r += 1
    write_form_field(ws, r, "Sistema/Projeto/Documento", 1, 2, 4, is_required=True)
    write_form_field(ws, r, "Data", 5, 6, NC)
    r += 1
    write_form_field(ws, r, "Verificador", 1, 2, 4)

    # Checklist — Dados de Treinamento
    r += 2
    write_section_header(ws, r, "SEÇÃO 1: DADOS DE TREINAMENTO E CONTEXTO  [Art. 20]", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Item de Verificação", "Referência", "Status", "Evidência", "Observações"])

    itens_treino = [
        ("Fontes de todos os datasets de treinamento identificadas e documentadas?", "Art. 20"),
        ("Licenças dos datasets verificadas e compatíveis com uso pretendido?", "Art. 20"),
        ("Autores/criadores dos conteúdos reconhecidos?", "Art. 21"),
        ("Dados externos à Câmara documentados para rastreabilidade?", "Art. 25-III-a"),
        ("Dados RAG com fontes documentadas e versionadas?", "Art. 25-III-b"),
        ("Nenhum conteúdo protegido por direito autoral utilizado sem autorização?", "Art. 4º-VIII"),
        ("Segredo industrial de terceiros preservado?", "Art. 4º-VIII"),
    ]
    for i, (item, ref) in enumerate(itens_treino, 1):
        r += 1
        write_checklist_row(ws, r, i, item, ref, NC)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Conforme", "Não conforme", "N/A"])

    # Checklist — Documentos Gerados por IA
    r += 2
    write_section_header(ws, r, "SEÇÃO 2: DOCUMENTOS PRODUZIDOS COM IA GENERATIVA  [Art. 21]", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Item de Verificação", "Referência", "Status", "Evidência", "Observações"])

    itens_docs = [
        ("Fontes dos dados indicadas no documento final?", "Art. 21"),
        ("Autores originais reconhecidos/citados?", "Art. 21"),
        ("Conteúdo gerado verificado factualmente?", "Art. 14"),
        ("Documento revisado antes de publicação/uso?", "Art. 14"),
        ("Atribuição de uso de IA incluída (disclosure)?", "Art. 12"),
        ("Em caso de colaboração com outros órgãos, fontes verificadas?", "Art. 21-Pú"),
    ]
    for i, (item, ref) in enumerate(itens_docs, 1):
        r += 1
        write_checklist_row(ws, r, i, item, ref, NC)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Conforme", "Não conforme", "N/A"])

    # Resultado
    r += 2
    write_section_header(ws, r, "RESULTADO", NC)
    r += 1
    write_form_field(ws, r, "Resultado geral", 1, 2, 3, is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Conforme", "Não conforme — ações necessárias", "Parcial"])
    write_form_field(ws, r, "Data", 4, 5, NC)
    r += 1
    write_form_field(ws, r, "Ações corretivas", 1, 2, NC)
    ws.row_dimensions[r].height = 50

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-10_Checklist_Fontes_Propriedade_Intelectual.xlsx")


def create_doc11():
    """DOC-11: Checklist de Avaliação para Contratação de Soluções com IA"""
    print("DOC-11: Checklist de Contratação de IA...")
    wb = new_workbook()
    ws = add_sheet(wb, "Contratação IA")
    NC = 6
    set_col_widths(ws, [5, 48, 16, 16, 22, 22])

    r = 1
    write_title_row(ws, r, "CHECKLIST DE AVALIAÇÃO PARA CONTRATAÇÃO DE SOLUÇÕES COM IA", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025 — Arts. 26§2º, 29-III", NC)

    # Identificação
    r += 2
    write_section_header(ws, r, "IDENTIFICAÇÃO DA SOLUÇÃO", NC)
    r += 1
    write_form_field(ws, r, "Nome da solução / fornecedor", 1, 2, NC, is_required=True)
    r += 1
    write_form_field(ws, r, "Unidade demandante", 1, 2, 4)
    write_form_field(ws, r, "Data", 5, 6, NC)
    r += 1
    write_form_field(ws, r, "Tipo de solução", 1, 2, NC)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["SaaS com IA", "Plataforma de IA", "API de IA", "Modelo pré-treinado",
                  "Solução customizada", "Outro"])
    r += 1
    write_form_field(ws, r, "Deliberação Ditec obtida?", 1, 2, 4, ref_artigo="Art. 29-III", is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim", "Não — pendente"])

    checklist_headers = ["#", "Item de Verificação", "Referência", "Status", "Evidência", "Observações"]

    # Seção 1: Análise Técnica
    r += 2
    write_section_header(ws, r, "SEÇÃO 1: ANÁLISE TÉCNICA", NC)
    r += 1
    write_col_headers(ws, r, checklist_headers)
    itens_tec = [
        ("Requisitos de negócio definidos e documentados?", "Art. 31-VII"),
        ("Avaliação de riscos éticos realizada e submetida ao CETIA?", "Art. 24"),
        ("Parecer do CETIA obtido?", "Art. 24§1º"),
        ("Testes de robustez planejados/exigidos do fornecedor?", "Art. 16"),
        ("Mecanismos de explicabilidade e rastreabilidade disponíveis?", "Art. 10"),
    ]
    for i, (item, ref) in enumerate(itens_tec, 1):
        r += 1
        write_checklist_row(ws, r, i, item, ref, NC)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Conforme", "Não conforme", "Parcial", "N/A"])

    # Seção 2: Conformidade Ética
    r += 2
    write_section_header(ws, r, "SEÇÃO 2: CONFORMIDADE COM PRINCÍPIOS ÉTICOS  [Art. 4º]", NC)
    r += 1
    write_col_headers(ws, r, checklist_headers)
    itens_etica = [
        ("Solução trata dados com boa fé e finalidade legítima?", "Art. 4º-I"),
        ("Privacidade e dados pessoais protegidos?", "Art. 4º-II"),
        ("Transparência dos procedimentos garantida?", "Art. 4º-III"),
        ("Responsabilização e prestação de contas asseguradas?", "Art. 4º-IV"),
        ("Resultados isentos de vieses e discriminação?", "Art. 4º-V"),
        ("Resiliência a falhas e incidentes?", "Art. 4º-VI"),
        ("Primazia da decisão humana preservada?", "Art. 4º-VII"),
        ("Propriedade intelectual respeitada?", "Art. 4º-VIII"),
    ]
    for i, (item, ref) in enumerate(itens_etica, 1):
        r += 1
        write_checklist_row(ws, r, i, item, ref, NC)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Conforme", "Não conforme", "Parcial", "N/A"])

    # Seção 3: Dados e Segurança
    r += 2
    write_section_header(ws, r, "SEÇÃO 3: DADOS, SEGURANÇA E LOCALIZAÇÃO", NC)
    r += 1
    write_col_headers(ws, r, checklist_headers)
    itens_dados = [
        ("Classificação dos dados envolvidos realizada?", "Arts. 17, 19§1º"),
        ("Localização do processamento identificada (nuvem pública/privada)?", "Arts. 2º XII-XIII"),
        ("Dados restritos excluídos de nuvem pública?", "Art. 19"),
        ("Dados pessoais em nuvem pública autorizados?", "Art. 8º"),
        ("SLAs de monitoramento definidos?", "Art. 27"),
        ("Procedimento de remoção do portfólio previsto no contrato?", "Art. 26§2º"),
    ]
    for i, (item, ref) in enumerate(itens_dados, 1):
        r += 1
        write_checklist_row(ws, r, i, item, ref, NC)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Conforme", "Não conforme", "Parcial", "N/A"])

    # Seção 4: Cláusulas Contratuais
    r += 2
    write_section_header(ws, r, "SEÇÃO 4: CLÁUSULAS DE GOVERNANÇA NO CONTRATO  [Art. 26§2º]", NC)
    r += 1
    write_col_headers(ws, r, checklist_headers)
    itens_contrato = [
        ("Cláusula de definição de requisitos e responsabilidades?", "Art. 26§2º"),
        ("Cláusula de monitoramento e relatórios periódicos?", "Art. 26§2º"),
        ("Cláusula de remoção/desativação do sistema?", "Art. 26§2º"),
        ("Cláusula de proteção de dados pessoais (LGPD)?", "Ato 152, Art. 7º"),
        ("Cláusula de vedação de dados restritos em nuvem pública?", "Art. 19"),
        ("Cláusula de transparência e explicabilidade?", "Arts. 10-11"),
    ]
    for i, (item, ref) in enumerate(itens_contrato, 1):
        r += 1
        write_checklist_row(ws, r, i, item, ref, NC)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Conforme", "Não conforme", "Parcial", "N/A"])

    # Parecer Ditec
    r += 2
    write_section_header(ws, r, "PARECER DA DITEC  [Art. 29-III]", NC)
    r += 1
    write_form_field(ws, r, "Parecer", 1, 2, NC, is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Favorável à contratação", "Favorável com condições",
                  "Desfavorável", "Requer análise adicional"])
    r += 1
    write_form_field(ws, r, "Condições / Justificativa", 1, 2, NC)
    ws.row_dimensions[r].height = 50
    r += 1
    write_form_field(ws, r, "Nome e assinatura — Ditec", 1, 2, 4)
    write_form_field(ws, r, "Data", 5, 6, NC)

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-11_Checklist_Contratacao_IA.xlsx")
