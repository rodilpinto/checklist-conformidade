# -*- coding: utf-8 -*-
"""
docs_lote1.py — Formulários (DOC-01, DOC-02, DOC-05)
"""
from docs_operacionais_helpers import *


def create_doc01():
    """DOC-01: Formulário de Solicitação e Autorização de Acesso a Dados para IA"""
    print("DOC-01: Formulário de Solicitação e Autorização de Acesso a Dados...")
    wb = new_workbook()
    ws = add_sheet(wb, "Solicitação Acesso Dados")
    NC = 6  # colunas: A-F
    set_col_widths(ws, [5, 28, 22, 22, 22, 22])

    r = 1
    write_title_row(ws, r, "FORMULÁRIO DE SOLICITAÇÃO E AUTORIZAÇÃO DE ACESSO A DADOS PARA IA", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025 — Arts. 7º§1º, 8º, 18, 30-I, 31-I, 32-I, 33", NC)

    # SEÇÃO 1: Identificação do Demandante
    r += 2
    write_section_header(ws, r, "1. IDENTIFICAÇÃO DO DEMANDANTE", NC)
    r += 1
    write_form_field(ws, r, "Unidade administrativa", 1, 2, NC, is_required=True)
    r += 1
    write_form_field(ws, r, "Nome do demandante", 1, 2, NC, is_required=True)
    r += 1
    write_form_field(ws, r, "Cargo/Função", 1, 2, 3)
    write_form_field(ws, r, "Ramal/E-mail", 4, 5, NC)
    r += 1
    write_form_field(ws, r, "Papel na governança de IA", 1, 2, NC, ref_artigo="Art. 28")
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Gestor de Negócio", "Gerente de Projeto", "Gestor de Dados", "Outro"])
    r += 1
    write_form_field(ws, r, "Data da solicitação", 1, 2, 3, is_required=True)

    # SEÇÃO 2: Sistema/Projeto de IA
    r += 2
    write_section_header(ws, r, "2. SISTEMA / PROJETO DE IA", NC)
    r += 1
    write_form_field(ws, r, "Nome do sistema/projeto de IA", 1, 2, NC, is_required=True)
    r += 1
    write_form_field(ws, r, "Descrição resumida", 1, 2, NC)
    r += 1
    write_form_field(ws, r, "Fase do ciclo de vida", 1, 2, NC, ref_artigo="Art. 2º, IV")
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Planejamento", "Desenho e Prototipação", "Coleta e Preparação de Dados",
                  "Modelagem e Treinamento", "Teste e Avaliação", "Implantação",
                  "Monitoramento e Feedback", "Desativação"])
    r += 1
    write_form_field(ws, r, "Parecer CETIA obtido?", 1, 2, 3, ref_artigo="Art. 24")
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim", "Não", "Em andamento", "N/A"])
    write_form_field(ws, r, "Nº do parecer", 4, 5, NC)

    # SEÇÃO 3: Dados Solicitados
    r += 2
    write_section_header(ws, r, "3. DADOS SOLICITADOS", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Dado / Dataset", "Fonte / Sistema",
                               "Classificação", "Gestor de Dados", "Finalidade"])
    # 5 linhas em branco para preenchimento
    for i in range(1, 6):
        r += 1
        fills = [None, fill_yellow(), fill_yellow(), fill_yellow(), fill_yellow(), fill_yellow()]
        write_data_row(ws, r, [i, "", "", "", "", ""], fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=4),
                     ["Público", "Pessoal", "Pessoal sensível", "Restrito", "Sigiloso"])

    # SEÇÃO 4: Classificação e Restrições
    r += 2
    write_section_header(ws, r, "4. CLASSIFICAÇÃO E RESTRIÇÕES", NC)
    r += 1
    write_form_field(ws, r, "Contém dados pessoais?", 1, 2, 3, ref_artigo="Art. 7º", is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim", "Não"])
    write_form_field(ws, r, "Contém dados pessoais sensíveis?", 4, 5, NC, ref_artigo="Art. 2º, XI")
    add_dropdown(ws, ws.cell(row=r, column=5), ["Sim", "Não"])
    r += 1
    write_form_field(ws, r, "Contém dados com restrição de acesso?", 1, 2, 3, ref_artigo="Art. 19§1º", is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim", "Não"])
    write_form_field(ws, r, "Categoria de restrição", 4, 5, NC)
    add_dropdown(ws, ws.cell(row=r, column=5),
                 ["Sigilo de Estado", "Sigilo legal", "Risco a processos corporativos",
                  "Credenciais de acesso", "N/A"])
    r += 1
    write_form_field(ws, r, "Ambiente de processamento", 1, 2, NC, ref_artigo="Arts. 2º XII-XIII, 19", is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Infraestrutura própria da Câmara", "Nuvem privada", "Nuvem pública"])
    r += 1
    write_form_field(ws, r, "Anonimização necessária?", 1, 2, 3, ref_artigo="Art. 7º§2º")
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim", "Não", "Já anonimizado"])
    write_form_field(ws, r, "Anonimização realizada?", 4, 5, NC)
    add_dropdown(ws, ws.cell(row=r, column=5), ["Sim", "Não", "N/A"])

    # SEÇÃO 5: Finalidade e Base Legal
    r += 2
    write_section_header(ws, r, "5. FINALIDADE E BASE LEGAL LGPD", NC)
    r += 1
    write_form_field(ws, r, "Finalidade do tratamento", 1, 2, NC, ref_artigo="Art. 4º, I", is_required=True)
    r += 1
    write_form_field(ws, r, "Base legal LGPD (se dados pessoais)", 1, 2, NC, ref_artigo="Art. 7º")
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Consentimento", "Obrigação legal", "Execução de políticas públicas",
                  "Legítimo interesse", "Proteção da vida", "Tutela da saúde",
                  "Exercício regular de direitos", "N/A — sem dados pessoais"])
    r += 1
    write_form_field(ws, r, "Justificativa formal para uso de dados pessoais", 1, 2, NC, ref_artigo="Art. 7º§1º")

    # SEÇÃO 6: Medidas de Proteção
    r += 2
    write_section_header(ws, r, "6. MEDIDAS DE PROTEÇÃO", NC)
    r += 1
    write_form_field(ws, r, "Controles de acesso previstos", 1, 2, NC, ref_artigo="Art. 17")
    r += 1
    write_form_field(ws, r, "Medidas de segurança da informação", 1, 2, NC, ref_artigo="Art. 16")
    r += 1
    write_form_field(ws, r, "Prazo de retenção dos dados", 1, 2, 3)
    write_form_field(ws, r, "Procedimento de exclusão", 4, 5, NC)

    # SEÇÃO 7: Vedações (alertas)
    r += 2
    write_section_header(ws, r, "7. VERIFICAÇÃO DE VEDAÇÕES", NC)
    r += 1
    vedacoes = [
        ("Dados pessoais em nuvem pública sem autorização do Gestor de Dados e Encarregado?", "Art. 8º"),
        ("Dados restritos em nuvem pública?", "Art. 19"),
        ("Minutas de documentos restritos em nuvem pública?", "Art. 19§3º"),
        ("Uso de e-mail corporativo para criar conta em IA não contratada?", "Art. 9º"),
    ]
    for vd_text, vd_art in vedacoes:
        r += 1
        ws.cell(row=r, column=1, value="⚠").font = font_normal()
        ws.cell(row=r, column=1).alignment = ALIGN_CENTER
        ws.cell(row=r, column=1).border = THIN_BORDER
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        ws.cell(row=r, column=2, value=vd_text).font = font_normal()
        ws.cell(row=r, column=2).alignment = ALIGN_LEFT
        ws.cell(row=r, column=2).border = THIN_BORDER
        for c in range(3, 5):
            ws.cell(row=r, column=c).border = THIN_BORDER
        ws.cell(row=r, column=5, value=vd_art).font = font_small()
        ws.cell(row=r, column=5).alignment = ALIGN_CENTER
        ws.cell(row=r, column=5).border = THIN_BORDER
        ws.cell(row=r, column=6).fill = fill_yellow()
        ws.cell(row=r, column=6).border = THIN_BORDER
        add_dropdown(ws, ws.cell(row=r, column=6), ["Não se aplica", "VEDADO — não prosseguir"])

    # SEÇÃO 8: Parecer do Gestor de Dados
    r += 2
    write_section_header(ws, r, "8. PARECER DO GESTOR DE DADOS  [Art. 30, I]", NC)
    r += 1
    write_form_field(ws, r, "Nome do Gestor de Dados", 1, 2, NC, is_required=True)
    r += 1
    write_form_field(ws, r, "Decisão", 1, 2, 3, ref_artigo="Art. 18", is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2), ["Autorizado", "Autorizado com condições", "Negado"])
    write_form_field(ws, r, "Data", 4, 5, NC)
    r += 1
    write_form_field(ws, r, "Condições / Justificativa", 1, 2, NC)

    # SEÇÃO 9: Parecer do Encarregado (se dados pessoais)
    r += 2
    write_section_header(ws, r, "9. PARECER DO ENCARREGADO DE DADOS PESSOAIS  [Art. 33]", NC)
    r += 1
    write_form_field(ws, r, "Nome do Encarregado", 1, 2, NC)
    r += 1
    write_form_field(ws, r, "Decisão", 1, 2, 3, ref_artigo="Art. 7º§1º", is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2), ["Autorizado", "Autorizado com condições", "Negado", "N/A"])
    write_form_field(ws, r, "Data", 4, 5, NC)
    r += 1
    write_form_field(ws, r, "Condições / Justificativa", 1, 2, NC)
    r += 1
    write_form_field(ws, r, "ROPA/RIPD necessário?", 1, 2, 3, ref_artigo="Portaria 226, Art. 15")
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim — ROPA", "Sim — ROPA + RIPD", "Não", "Já existente"])

    # SEÇÃO 10: Aprovação Final
    r += 2
    write_section_header(ws, r, "10. APROVAÇÃO FINAL", NC)
    r += 1
    write_form_field(ws, r, "Status da solicitação", 1, 2, NC, is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Aprovado", "Aprovado com condições", "Negado — aguardando parecer CETIA",
                  "Negado — vedação aplicável", "Em análise"])
    r += 1
    write_form_field(ws, r, "Observações finais", 1, 2, NC)

    # SEÇÃO 11: Assinaturas
    r += 2
    write_section_header(ws, r, "11. ASSINATURAS", NC)
    assinaturas = [
        ("Demandante", 1, 3), ("Gestor de Dados", 4, NC),
        ("Encarregado de Dados Pessoais (se aplicável)", 1, 3), ("Aprovador final", 4, NC),
    ]
    for i in range(0, len(assinaturas), 2):
        r += 1
        for nome, c_start, c_end in assinaturas[i:i+2]:
            ws.merge_cells(start_row=r, start_column=c_start, end_row=r, end_column=c_end)
            cell = ws.cell(row=r, column=c_start, value=nome)
            cell.font = font_label()
            cell.alignment = ALIGN_CENTER
            cell.border = THIN_BORDER
            for c in range(c_start + 1, c_end + 1):
                ws.cell(row=r, column=c).border = THIN_BORDER
        r += 1
        for nome, c_start, c_end in assinaturas[i:i+2]:
            ws.merge_cells(start_row=r, start_column=c_start, end_row=r, end_column=c_end)
            cell = ws.cell(row=r, column=c_start, value="Assinatura: ")
            cell.font = font_normal()
            cell.fill = fill_yellow()
            cell.border = THIN_BORDER
            for c in range(c_start + 1, c_end + 1):
                ws.cell(row=r, column=c).border = THIN_BORDER
                ws.cell(row=r, column=c).fill = fill_yellow()
        ws.row_dimensions[r].height = 40

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-01_Formulario_Solicitacao_Acesso_Dados_IA.xlsx")


def create_doc02():
    """DOC-02: Formulário de Avaliação de Riscos Éticos de IA (pré-CETIA)"""
    print("DOC-02: Formulário de Avaliação de Riscos Éticos...")
    wb = new_workbook()
    ws = add_sheet(wb, "Avaliação Riscos Éticos")
    NC = 7
    set_col_widths(ws, [5, 32, 18, 14, 14, 18, 22])

    r = 1
    write_title_row(ws, r, "FORMULÁRIO DE AVALIAÇÃO DE RISCOS ÉTICOS DE IA (PRÉ-CETIA)", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025 — Arts. 4º, 5º-Pú, 15, 22, 24, 26§3-§4", NC)

    # Seção 1: Identificação do Projeto
    r += 2
    write_section_header(ws, r, "1. IDENTIFICAÇÃO DO PROJETO / DEMANDA", NC)
    r += 1
    write_form_field(ws, r, "Nome do projeto/sistema de IA", 1, 2, NC, is_required=True)
    r += 1
    write_form_field(ws, r, "Unidade demandante", 1, 2, 4, is_required=True)
    write_form_field(ws, r, "Data", 5, 6, NC, is_required=True)
    r += 1
    write_form_field(ws, r, "Responsável pela avaliação (Ditec)", 1, 2, NC, ref_artigo="Art. 24, caput")
    r += 1
    write_form_field(ws, r, "Descrição resumida da IA", 1, 2, NC)
    ws.row_dimensions[r].height = 50
    r += 1
    write_form_field(ws, r, "Tipo de IA", 1, 2, 4)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["IA Generativa", "IA Preditiva", "IA Classificatória",
                  "Agente de IA", "RAG", "Outro"])
    write_form_field(ws, r, "Ambiente", 5, 6, NC, ref_artigo="Arts. 2º XII-XIII")
    add_dropdown(ws, ws.cell(row=r, column=6), ["Infra própria", "Nuvem privada", "Nuvem pública", "Híbrido"])

    # Seção 2: Princípios Éticos (Art. 4º)
    r += 2
    write_section_header(ws, r, "2. AVALIAÇÃO POR PRINCÍPIO ÉTICO  [Art. 4º]", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Princípio Ético (Art. 4º)", "Inciso",
                               "Nível de Risco", "Justificativa", "Mitigação Proposta", "Status"])

    principios = [
        ("I", "Tratamento de dados com boa fé e finalidade legítima"),
        ("II", "Proteção do direito à privacidade e dos dados pessoais"),
        ("III", "Transparência e publicidade responsável dos procedimentos e decisões"),
        ("IV", "Responsabilização e prestação de contas"),
        ("V", "Resultados justos, isentos de vieses, inclusivos e não discriminatórios"),
        ("VI", "Operação conforme propósitos, dados íntegros, acessos autorizados, resiliência a falhas e incidentes"),
        ("VII", "Primazia da decisão humana, autonomia no uso e supervisão contínua"),
        ("VIII", "Respeito à propriedade intelectual, segredo industrial e direitos autorais"),
    ]
    for i, (inciso, texto) in enumerate(principios, 1):
        r += 1
        fills = [None, None, None, fill_yellow(), fill_yellow(), fill_yellow(), fill_yellow()]
        write_data_row(ws, r, [i, texto, inciso, "", "", "", ""], fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=4),
                     ["Crítico", "Alto", "Médio", "Baixo", "N/A"])
        add_dropdown(ws, ws.cell(row=r, column=7),
                     ["Mitigado", "Em mitigação", "Aceito", "Pendente"])
        ws.row_dimensions[r].height = 35

    # Seção 3: Riscos do Art. 5º-Pú
    r += 2
    write_section_header(ws, r, "3. RISCOS DE USO INADEQUADO  [Art. 5º, Parágrafo único]", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Categoria de Risco", "Inciso",
                               "Aplicável?", "Nível de Risco", "Mitigação Proposta", "Status"])
    riscos_5 = [
        ("I", "Comprometer direitos fundamentais"),
        ("II", "Violar a privacidade ou a autonomia das pessoas"),
        ("III", "Causar danos à integridade física, psicológica ou financeira dos indivíduos"),
        ("IV", "Prejudicar instituições"),
        ("V", "Ameaçar a segurança, a confiança social ou a estabilidade democrática"),
        ("VI", "Produzir conteúdos falsos ou desinformação"),
        ("VII", "Produzir ou ampliar vieses, discriminação e decisões injustas"),
    ]
    for i, (inciso, texto) in enumerate(riscos_5, 1):
        r += 1
        fills = [None, None, None, fill_yellow(), fill_yellow(), fill_yellow(), fill_yellow()]
        write_data_row(ws, r, [i, texto, inciso, "", "", "", ""], fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Sim", "Não"])
        add_dropdown(ws, ws.cell(row=r, column=5), ["Crítico", "Alto", "Médio", "Baixo", "N/A"])
        add_dropdown(ws, ws.cell(row=r, column=7), ["Mitigado", "Em mitigação", "Aceito", "Pendente"])

    # Seção 4: Vedações (Art. 15)
    r += 2
    write_section_header(ws, r, "4. VERIFICAÇÃO DE VEDAÇÕES  [Art. 15]", NC)
    r += 1
    write_col_headers(ws, r, ["#", "Vedação", "Inciso",
                               "Aplicável?", "Resultado", "Evidência", "Obs."])
    vedacoes_15 = [
        ("I", "Gerar resultados discriminatórios ilícitos ou abusivos"),
        ("II", "Criar ou reforçar vieses contra qualquer entidade representada nos dados"),
        ("III", "Valorar traços de personalidade ou características de comportamento para avaliação de perfis"),
    ]
    for i, (inciso, texto) in enumerate(vedacoes_15, 1):
        r += 1
        fills = [None, None, None, fill_yellow(), fill_yellow(), fill_yellow(), fill_yellow()]
        write_data_row(ws, r, [i, texto, inciso, "", "", "", ""], fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=4), ["Sim — VEDADO", "Não se aplica"])
        add_dropdown(ws, ws.cell(row=r, column=5), ["Conforme", "VEDAÇÃO APLICÁVEL"])

    # Seção 5: Dados envolvidos
    r += 2
    write_section_header(ws, r, "5. DADOS ENVOLVIDOS", NC)
    r += 1
    write_form_field(ws, r, "Dados pessoais envolvidos?", 1, 2, 4, ref_artigo="Art. 7º")
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim", "Não"])
    write_form_field(ws, r, "Dados restritos?", 5, 6, NC, ref_artigo="Art. 19")
    add_dropdown(ws, ws.cell(row=r, column=6), ["Sim", "Não"])
    r += 1
    write_form_field(ws, r, "Nuvem pública envolvida?", 1, 2, 4, ref_artigo="Arts. 8º, 19")
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim", "Não"])
    r += 1
    write_form_field(ws, r, "Resumo dos dados e classificação", 1, 2, NC)

    # Seção 6: Riscos de segurança (Art. 26§3)
    r += 2
    write_section_header(ws, r, "6. RISCOS DE SEGURANÇA E FALHAS  [Art. 26, §3º]", NC)
    r += 1
    write_form_field(ws, r, "Riscos de incidentes de segurança identificados", 1, 2, NC, is_required=True)
    ws.row_dimensions[r].height = 50
    r += 1
    write_form_field(ws, r, "Riscos de falhas identificados", 1, 2, NC, is_required=True)
    ws.row_dimensions[r].height = 50
    r += 1
    write_form_field(ws, r, "Plano de testes para detectar comportamentos inadequados", 1, 2, NC, ref_artigo="Art. 26§3º")
    ws.row_dimensions[r].height = 50

    # Seção 7: Vieses e alucinações (Art. 26§4)
    r += 2
    write_section_header(ws, r, "7. CONTROLE DE VIESES E ALUCINAÇÕES  [Art. 26, §4º]", NC)
    r += 1
    write_form_field(ws, r, "Medidas de identificação e controle de vieses", 1, 2, NC, is_required=True)
    ws.row_dimensions[r].height = 50
    r += 1
    write_form_field(ws, r, "Medidas de controle de alucinações", 1, 2, NC)
    ws.row_dimensions[r].height = 50

    # Seção 8: Classificação Global de Risco
    r += 2
    write_section_header(ws, r, "8. CLASSIFICAÇÃO GLOBAL DE RISCO", NC)
    r += 1
    write_form_field(ws, r, "Classificação global de risco", 1, 2, 4, is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Crítico — rejeição automática (Art. 24§2)",
                  "Alto — requer condições rigorosas",
                  "Médio — condições padrão",
                  "Baixo — aprovação simplificada"])
    r += 1
    write_form_field(ws, r, "Justificativa da classificação", 1, 2, NC)
    ws.row_dimensions[r].height = 50

    # Seção 9: Parecer Ditec
    r += 2
    write_section_header(ws, r, "9. PARECER DA DITEC  [Art. 24, caput]", NC)
    r += 1
    write_form_field(ws, r, "Parecer da Ditec", 1, 2, NC, is_required=True)
    add_dropdown(ws, ws.cell(row=r, column=2),
                 ["Encaminhar ao CETIA — risco aceitável com condições",
                  "Encaminhar ao CETIA — alto risco, requer análise aprofundada",
                  "Não encaminhar — vedação aplicável",
                  "Não encaminhar — projeto inviável"])
    r += 1
    write_form_field(ws, r, "Condições propostas pela Ditec", 1, 2, NC)
    ws.row_dimensions[r].height = 50
    r += 1
    write_form_field(ws, r, "Consulta ao CGSIC necessária?", 1, 2, 4, ref_artigo="Art. 24§3º")
    add_dropdown(ws, ws.cell(row=r, column=2), ["Sim — aspectos de segurança envolvidos", "Não"])
    r += 1
    write_form_field(ws, r, "Nome / Assinatura — Ditec", 1, 2, 4, is_required=True)
    write_form_field(ws, r, "Data", 5, 6, NC)

    # Seção 10: Encaminhamento ao CETIA
    r += 2
    write_section_header(ws, r, "10. ENCAMINHAMENTO AO CETIA  [Art. 24]", NC)
    r += 1
    write_form_field(ws, r, "Data de encaminhamento", 1, 2, 4)
    write_form_field(ws, r, "Nº do protocolo", 5, 6, NC)
    r += 1
    write_form_field(ws, r, "Documentos anexados", 1, 2, NC)

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-02_Formulario_Avaliacao_Riscos_Eticos_IA.xlsx")


def create_doc05():
    """DOC-05: Mapeamento e Classificação de Dados do Projeto de IA"""
    print("DOC-05: Mapeamento e Classificação de Dados...")
    wb = new_workbook()
    ws = add_sheet(wb, "Mapeamento Dados IA")
    NC = 10
    set_col_widths(ws, [5, 22, 18, 18, 16, 18, 18, 14, 14, 22])

    r = 1
    write_title_row(ws, r, "MAPEAMENTO E CLASSIFICAÇÃO DE DADOS DO PROJETO DE IA", NC, 40)
    r += 1
    write_subtitle_row(ws, r, "Portaria 227/2025 — Arts. 6º, 7º, 8º, 17, 18, 19", NC)

    # Identificação do projeto
    r += 2
    write_section_header(ws, r, "IDENTIFICAÇÃO DO PROJETO", NC)
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
    write_form_field(ws, r, "Projeto / Sistema de IA", 1, 3, 6, is_required=True)
    write_form_field(ws, r, "Data", 7, 8, 10)
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
    write_form_field(ws, r, "Responsável pelo mapeamento", 1, 3, 6)
    write_form_field(ws, r, "Unidade", 7, 8, 10)

    # Tabela de mapeamento
    r += 2
    write_section_header(ws, r, "MAPEAMENTO DE DADOS", NC)
    r += 1
    headers = [
        "#",
        "Nome do Dado",
        "Fonte / Sistema",
        "Classificação\n[Arts. 7º, 19§1º]",
        "Base Legal LGPD\n[Art. 7º]",
        "Gestor de Dados\nResponsável",
        "Ambiente\n[Arts. 2º XII-XIII]",
        "Autorização\nObtida?\n[Art. 18]",
        "Anonimização\nNecessária?\n[Art. 7º§2º]",
        "Observações"
    ]
    write_col_headers(ws, r, headers)

    classificacoes = ["Público", "Pessoal", "Pessoal sensível",
                      "Restrito — sigilo de Estado", "Restrito — sigilo legal",
                      "Restrito — risco a processos", "Restrito — credenciais"]
    bases_lgpd = ["Consentimento", "Obrigação legal", "Execução de políticas públicas",
                  "Legítimo interesse", "N/A — sem dados pessoais"]
    ambientes = ["Infraestrutura própria", "Nuvem privada", "Nuvem pública"]
    sim_nao = ["Sim", "Não", "N/A"]

    for i in range(1, 21):
        r += 1
        fills = [None] + [fill_yellow()] * 9
        write_data_row(ws, r, [i] + [""] * 9, fills=fills)
        add_dropdown(ws, ws.cell(row=r, column=4), classificacoes)
        add_dropdown(ws, ws.cell(row=r, column=5), bases_lgpd)
        add_dropdown(ws, ws.cell(row=r, column=7), ambientes)
        add_dropdown(ws, ws.cell(row=r, column=8), sim_nao)
        add_dropdown(ws, ws.cell(row=r, column=9), sim_nao)

    # Resumo
    r += 2
    write_section_header(ws, r, "RESUMO E ALERTAS", NC)
    r += 1
    write_form_field(ws, r, "Total de dados mapeados", 1, 3, 4)
    write_form_field(ws, r, "Dados pessoais", 5, 7, 7)
    write_form_field(ws, r, "Dados restritos", 8, 9, 10)
    r += 1
    alerts = [
        "ALERTA: Dados pessoais em nuvem pública requerem autorização do Gestor de Dados E do Encarregado (Art. 8º)",
        "ALERTA: Dados restritos são VEDADOS em nuvem pública (Art. 19)",
        "ALERTA: O uso de dados pessoais deve ser evitado — documentar justificativa se necessário (Art. 6º)"
    ]
    for alert in alerts:
        r += 1
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=NC)
        cell = ws.cell(row=r, column=1, value=alert)
        cell.font = Font(name='Arial', size=9, italic=True, color="CC0000")
        cell.fill = PatternFill(start_color="FFF0F0", end_color="FFF0F0", fill_type='solid')
        cell.alignment = ALIGN_LEFT
        cell.border = THIN_BORDER
        for c in range(2, NC + 1):
            ws.cell(row=r, column=c).border = THIN_BORDER
            ws.cell(row=r, column=c).fill = PatternFill(start_color="FFF0F0", end_color="FFF0F0", fill_type='solid')

    r += 2
    write_footer(ws, r, NC)

    save_xlsx(wb, "DOC-05_Mapeamento_Classificacao_Dados_IA.xlsx")
