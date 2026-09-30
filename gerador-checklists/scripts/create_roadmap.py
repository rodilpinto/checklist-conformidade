import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()

HEADER_FILL = PatternFill('solid', fgColor='1F4E79')
HEADER_FONT = Font(name='Arial', bold=True, color='FFFFFF', size=10)
SUBHEADER_FILL = PatternFill('solid', fgColor='D6E4F0')
DATA_FONT = Font(name='Arial', size=10)
BOLD_FONT = Font(name='Arial', bold=True, size=10)
WRAP = Alignment(wrap_text=True, vertical='top')
WRAP_C = Alignment(wrap_text=True, vertical='top', horizontal='center')
BORDER = Border(left=Side('thin'), right=Side('thin'), top=Side('thin'), bottom=Side('thin'))
GREEN = PatternFill('solid', fgColor='C6EFCE')
YELLOW = PatternFill('solid', fgColor='FFEB9C')
ORANGE = PatternFill('solid', fgColor='FCD5B4')
RED = PatternFill('solid', fgColor='FFC7CE')

def style_header(ws, headers, widths):
    for i, (h, w) in enumerate(zip(headers, widths), 1):
        c = ws.cell(row=1, column=i, value=h)
        c.font = HEADER_FONT
        c.fill = HEADER_FILL
        c.alignment = WRAP_C
        c.border = BORDER
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = 'A2'

def style_rows(ws, data, start=2, center_cols=None):
    for i, row in enumerate(data, start):
        for j, val in enumerate(row, 1):
            c = ws.cell(row=i, column=j, value=val)
            c.font = DATA_FONT
            c.alignment = WRAP
            c.border = BORDER
        if center_cols:
            for col in center_cols:
                ws.cell(row=i, column=col).alignment = WRAP_C

# ── Sheet 1: Roadmap ──
ws = wb.active
ws.title = 'Roadmap Automacao'

hdrs = ['ID', 'Teste (Grupo)', 'N Ordem', 'Passo', 'Descricao do Passo', 'Papel de Trabalho',
        'Tipo de Dados', 'Sensibilidade', 'Decisao Humana?', 'Natureza', 'Potencial Automacao',
        'Solucao Proposta', 'Complexidade Impl.', 'Prioridade', 'Dependencias', 'Observacoes']
wids = [5, 25, 8, 45, 55, 25, 18, 16, 16, 22, 20, 42, 16, 12, 30, 40]
style_header(ws, hdrs, wids)

data = [
    # === Formalizacao (Teste order 1) ===
    (1, 'Formalizacao', 1,
     'Solicitacao de informacoes a gestao',
     'Elaborar e encaminhar memorando para solicitacao formal de documentos e acesso necessarios ao entendimento do objeto.',
     'Memorando de solicitacao', 'Publicos internos', 'Baixa', 'Nao',
     'Burocratica', 'Alto',
     'Template inteligente: gerar memorando a partir de campos estruturados (objeto, unidade, docs solicitados). Integrar com Sicoi.',
     'Baixa', 'Alta', 'Definicao previa do objeto',
     'Texto padrao com poucas variaveis. Candidato ideal para template parametrizado.'),

    (2, 'Formalizacao', 2,
     'Comunicacao formal de apresentacao (PT0)',
     'Elaborar e enviar memorando formal a unidade auditada apresentando equipe, objeto e periodo, usando PT0 Memorando de comunicacao.docx.',
     'PT0 Memorando de comunicacao.docx', 'Publicos internos', 'Baixa', 'Nao',
     'Burocratica', 'Alto',
     'Geracao automatica do PT0 a partir de dados do Sicoi (equipe, objeto, cronograma). Formulario web ou chatbot.',
     'Baixa', 'Alta', 'ID 1; definicao de equipe (ID 3)',
     'Documento 100% padronizado. Automacao plena viavel.'),

    (3, 'Formalizacao', 3,
     'Definicao da equipe e cronograma',
     'Definir auditores responsaveis e elaborar cronograma detalhado com prazos das principais etapas.',
     'Cronograma no Sicoi', 'Publicos internos', 'Baixa', 'Sim',
     'Decisoria/Gerencial', 'Parcial',
     'Sugerir equipe por disponibilidade/especialidade (Sicoi). Gerar cronograma-modelo com marcos padrao. Decisao final humana.',
     'Media', 'Media', 'Aprovacao do chefe de nucleo',
     'Alocacao de pessoas e humana; sugestao baseada em dados e possivel.'),

    # === Entendimento do objeto (Teste order 2) ===
    (4, 'Entendimento do objeto', 1,
     'Objetivo, contextualizacao, materialidade',
     'Definir objetivo geral, contextualizar o objeto e identificar objetivos institucionais (conformidade, operacional, divulgacao), secoes 1-3 do PT1.',
     'PT1 (secoes 1-3)', 'Publicos + possivel sigiloso', 'Media', 'Sim',
     'Analitica/Decisoria', 'Parcial',
     'IA coleta dados orcamentarios (SIAFI/Siorc), planejamento estrategico, e gera rascunho. Auditor valida com julgamento profissional.',
     'Media', 'Alta', 'Primeiro passo substantivo; alimenta todos os demais',
     'Materialidade pode envolver dados orcamentarios sensiveis. Objetivos requerem julgamento.'),

    (5, 'Entendimento do objeto', 2,
     'Descritivo do processo (entradas, etapas, saidas)',
     'Elaborar descricao sequencial do fluxo do processo, identificando entradas, etapas criticas, responsaveis e saidas, secao 7 do PT1.',
     'PT1 (secao 7)', 'Publicos internos', 'Baixa', 'Parcial',
     'Analitica/Descritiva', 'Parcial',
     'IA compila normativos internos, manuais e fluxogramas existentes para gerar rascunho descritivo. Auditor valida com gestor.',
     'Media', 'Alta', 'ID 4; alimenta diagrama de escopo (ID 8)',
     'Se existirem fluxogramas previos (BPMN, Visio), extracao pode ser bastante automatizada.'),

    (6, 'Entendimento do objeto', 3,
     'Recursos de suporte (sistemas, pessoas, contratos, infra)',
     'Identificar recursos necessarios ao processo (sistemas, servidores, contratos, infraestrutura), secao 6 do PT1.',
     'PT1 (secao 6)', 'Publicos + dado pessoal', 'Media', 'Parcial',
     'Pesquisa/Descritiva', 'Parcial',
     'Consultar bases de contratos (DW-Compras), catalogo de sistemas (CENIN), e-Pessoal para inventario automatizado. Auditor valida.',
     'Media', 'Media', 'ID 4; paralelo com ID 5',
     'Nomes de servidores e contratos podem conter dados pessoais (LGPD).'),

    (7, 'Entendimento do objeto', 4,
     'Validacao do diagrama de escopo com gestor',
     'Apresentar e validar Diagrama de Escopo junto ao gestor responsavel, registrando ajustes no PT1.',
     'PT1', 'Publicos internos', 'Baixa', 'Sim',
     'Interacao humana', 'Baixo',
     'Disponibilizar diagrama online para revisao/comentarios com controle de versao. Agendamento via Sicoi.',
     'Media', 'Baixa', 'ID 8, ID 9',
     'Atividade humana: negociacao, explicacao, alinhamento presencial.'),

    (8, 'Entendimento do objeto', 5,
     'Elaboracao do diagrama de escopo',
     'Construir Diagrama de Escopo consolidando informacoes das etapas anteriores, Apendice 1 do PT1.',
     'PT1 (Apendice 1)', 'Publicos internos', 'Baixa', 'Parcial',
     'Sintese/Diagramacao', 'Parcial',
     'IA gera rascunho a partir de dados coletados (objetivos, reguladores, processos, recursos, RECI). Auditor ajusta.',
     'Alta', 'Alta', 'IDs 4,5,6,10,11',
     'Principal entregavel do entendimento. Automacao parcial poupa tempo significativo.'),

    (9, 'Entendimento do objeto', 6,
     'Reuniao com Secretaria para validar diagrama de escopo',
     'Reuniao de alinhamento interno com a Secretaria para validacao preliminar do Diagrama de Escopo.',
     'PT1', 'Publicos internos', 'Baixa', 'Sim',
     'Interacao humana', 'Baixo',
     'Automacao de agendamento e geracao de pauta/ata modelo. Briefing automatico com resumo do diagrama.',
     'Baixa', 'Baixa', 'ID 8',
     'Reuniao hierarquica - decisao 100% humana. Suporte logistico automatizavel.'),

    (10, 'Entendimento do objeto', 7,
     'Consolidacao do entendimento do objeto',
     'Integrar e consolidar todas as informacoes coletadas sobre o objeto nos papeis de trabalho do PT1.',
     'PT1', 'Publicos + possivel sigiloso', 'Media', 'Parcial',
     'Sintese/Compilacao', 'Parcial',
     'IA compila secoes do PT1 ja preenchidas, verifica completude e consistencia, gera versao consolidada. Auditor revisa.',
     'Media', 'Alta', 'Todos os passos IDs 4-9',
     'Compilacao: alta oportunidade de automacao. Verificacao de consistencia e valor agregado.'),

    (11, 'Entendimento do objeto', 8,
     'Identificacao dos marcos regulatorios',
     'Levantar e analisar legislacao, regulamentos internos e externos aplicaveis ao objeto, secao 5 do PT1.',
     'PT1 (secao 5)', 'Publicos', 'Baixa', 'Parcial',
     'Pesquisa/Analitica', 'Alto',
     'Busca automatizada em bases legislativas (LexML, portais internos). IA classifica relevancia e gera lista estruturada. Auditor valida.',
     'Media', 'Alta', 'Paralelo com ID 4; alimenta riscos',
     'Dados 100% publicos. Alta automacao possivel com NLP em bases legislativas.'),

    (12, 'Entendimento do objeto', 9,
     'Participantes e competencias, Matriz RECI',
     'Mapear atores envolvidos e elaborar Matriz RECI, secao 4 e Apendice 2 do PT1.',
     'PT1 (secao 4 + Apendice 2)', 'Dados pessoais', 'Alta', 'Parcial',
     'Pesquisa/Mapeamento', 'Parcial',
     'Consultar organograma e RH para pre-popular RECI com cargos/atribuicoes regimentais. Auditor ajusta via entrevistas.',
     'Media', 'Media', 'ID 5',
     'Contem dados pessoais (LGPD): nomes, cargos, lotacoes.'),

    # === Identificacao de riscos (Teste order 3) ===
    (13, 'Identificacao de riscos', 1,
     'Avaliacao dos riscos inerentes, identificacao dos significativos',
     'Analisar cada risco quanto a probabilidade e impacto, priorizando os significativos na aba "R. relevantes" do PT2.',
     'PT2 (aba R. relevantes)', 'Publicos + julgamento', 'Baixa', 'Sim',
     'Analitica/Decisoria', 'Parcial',
     'IA sugere riscos com base em COSO e trabalhos anteriores. Calculo de criticidade automatizado. Priorizacao e do auditor.',
     'Alta', 'Alta', 'IDs 4-12',
     'Julgamento sobre probabilidade/impacto e humano. IA acelera identificacao inicial.'),

    (14, 'Identificacao de riscos', 2,
     'Riscos inerentes relevantes e vinculacao aos objetivos',
     'Identificar riscos inerentes relevantes e associa-los aos objetivos do objeto (conformidade, operacional, divulgacao) no PT2.',
     'PT2 (aba R. relevantes)', 'Publicos + julgamento', 'Baixa', 'Sim',
     'Analitica/Decisoria', 'Parcial',
     'IA gera lista preliminar de riscos a partir do processo, reguladores e trabalhos anteriores. Vinculacao a categorias COSO sugerida automaticamente.',
     'Alta', 'Alta', 'IDs 4,5,11; alimenta ID 13',
     'Identificacao de riscos e core - assistencia de IA valiosa mas decisao e humana.'),

    # === Avaliacao de controles (Teste order 4) ===
    (15, 'Avaliacao de controles', 1,
     'Identificacao de controles chave associados aos riscos significativos',
     'Identificar e registrar controles internos chave para mitigacao dos riscos significativos na aba "Avaliacao" do PT3.',
     'PT3 (aba Avaliacao)', 'Publicos internos', 'Baixa', 'Sim',
     'Analitica/Mapeamento', 'Parcial',
     'IA sugere controles tipicos por tipo de risco (COSO/COBIT). PT3 com campos pre-populados. Auditor confirma existencia real.',
     'Alta', 'Alta', 'IDs 13, 14',
     'Identificacao requer conhecimento do processo real - entrevistas essenciais.'),

    (16, 'Avaliacao de controles', 2,
     'Testes de desenho e de implementacao dos controles',
     'Executar testes de desenho e implementacao dos controles chave, registrando resultados na aba "Avaliacao" do PT3.',
     'PT3 (aba Avaliacao)', 'Publicos + possivel sigiloso', 'Media', 'Sim',
     'Analitica/Teste', 'Parcial',
     'Checklist digital estruturado para testes de desenho e implementacao. Registro padronizado de evidencias.',
     'Alta', 'Alta', 'ID 15',
     'Testes requerem julgamento profissional. Formularios estruturados aceleram registro.'),

    (17, 'Avaliacao de controles', 3,
     'Reuniao com Secretaria para validar diagrama processos/riscos/controles',
     'Reuniao interna com a Secretaria para validacao do diagrama integrado, registrando ata no PT3.',
     'PT3 (ata)', 'Publicos internos', 'Baixa', 'Sim',
     'Interacao humana', 'Baixo',
     'Briefing automatico (resumo do diagrama, riscos, controles). Modelo de ata pre-preenchido.',
     'Baixa', 'Baixa', 'IDs 15, 16',
     'Decisao hierarquica - 100% humana. Suporte logistico automatizavel.'),

    (18, 'Avaliacao de controles', 4,
     'Elaboracao do diagrama de processos, riscos e controles',
     'Elaborar/atualizar diagrama integrado de processos, riscos e controles, inserindo no PT3.',
     'PT3', 'Publicos internos', 'Baixa', 'Parcial',
     'Sintese/Diagramacao', 'Parcial',
     'IA gera rascunho integrando PT1 (processos), PT2 (riscos) e PT3 (controles). Visualizacao interativa para ajustes.',
     'Alta', 'Alta', 'IDs 8,13-16',
     'Diagrama integrado e entregavel de alto valor. Geracao assistida por IA poupa dias.'),

    (19, 'Avaliacao de controles', 5,
     'Validacao do diagrama com gestor do objeto auditado',
     'Apresentar e validar diagrama integrado junto ao gestor, registrando ajustes no PT3.',
     'PT3 (validacao)', 'Publicos internos', 'Baixa', 'Sim',
     'Interacao humana', 'Baixo',
     'Ferramenta colaborativa para revisao online do diagrama. Controle de versao e registro de comentarios.',
     'Media', 'Baixa', 'IDs 17, 18',
     'Atividade humana de negociacao e validacao com contraditorio.'),

    # === Avaliacao de riscos (Teste order 5) ===
    (20, 'Avaliacao de riscos', 1,
     'Risco significativo x risco de controle = risco residual',
     'Avaliar adequacao e efetividade dos controles para determinar risco residual de cada risco significativo no PT3.',
     'PT3 (aba Avaliacao)', 'Publicos + julgamento', 'Baixa', 'Sim',
     'Analitica/Calculo', 'Parcial',
     'Calculo automatico do risco residual (risco inerente x efetividade controle). Dashboard visual de mapa de calor. Classificacao e do auditor.',
     'Media', 'Alta', 'IDs 13-16',
     'Calculo e automatizavel; julgamento sobre efetividade e humano.'),

    # === Objetivos especificos e escopo (Teste order 6) ===
    (21, 'Objetivos especificos e escopo', 1,
     'Objetivos especificos, escopo e questoes de auditoria',
     'Definir objetivos especificos e formular questoes de auditoria, secoes 3 e 4 do PT5.',
     'PT5 (secoes 3-4)', 'Publicos internos', 'Baixa', 'Sim',
     'Decisoria/Estrategica', 'Parcial',
     'IA sugere questoes baseadas nos riscos residuais mais altos e banco de questoes de trabalhos anteriores. Auditor formula e prioriza.',
     'Alta', 'Alta', 'ID 20',
     'Formulacao de questoes e competencia core do auditor. IA e apoio.'),

    (22, 'Objetivos especificos e escopo', 2,
     'Reuniao com Secretaria para validar objetivos e escopo',
     'Reuniao final com Secretaria para validacao integrada: diagrama, objetivos, questoes e escopo, registrando no PT5.',
     'PT5', 'Publicos internos', 'Baixa', 'Sim',
     'Interacao humana', 'Baixo',
     'Briefing executivo consolidando diagrama, riscos residuais, objetivos, questoes e escopo. Ata pre-preenchida.',
     'Baixa', 'Baixa', 'IDs 18-21',
     'Reuniao de decisao estrategica - essencialmente humana.'),

    # === Programacao da execucao (Teste order 7) ===
    (23, 'Programacao da execucao', 1,
     'Definicao dos testes de controle e substantivos',
     'Definir testes de controles e substantivos para a fase de execucao na aba "Programa de auditoria" do PT6.',
     'PT6 (aba Programa)', 'Publicos internos', 'Baixa', 'Sim',
     'Decisoria/Tecnica', 'Parcial',
     'IA sugere testes padrao por tipo de controle/risco (IPPF/IIA). Banco de testes reutilizaveis. Auditor seleciona e adapta.',
     'Alta', 'Alta', 'IDs 20, 21',
     'Definicao de procedimentos e julgamento profissional. Base de conhecimento acelera.'),

    (24, 'Programacao da execucao', 2,
     'Tecnica de amostragem e plano amostral',
     'Escolher tecnica de amostragem e elaborar plano amostral detalhado na aba "Programa de auditoria" do PT6.',
     'PT6 (aba Programa)', 'Publicos internos', 'Baixa', 'Parcial',
     'Tecnica/Estatistica', 'Alto',
     'Calculadora de amostragem integrada: universo, confianca, erro toleravel -> tamanho amostral. Selecao aleatoria automatizada.',
     'Media', 'Alta', 'ID 23',
     'Calculo amostral e 100% automatizavel. Decisao sobre parametros e do auditor.'),

    (25, 'Programacao da execucao', 3,
     'R1 - Folha descritiva dos testes (PT7)',
     'Elaborar folha descritiva com procedimentos detalhados para testes de controle e substantivos do risco R1, usando PT7.',
     'PT7 Folha de teste.doc', 'Publicos internos', 'Baixa', 'Parcial',
     'Redacao/Tecnica', 'Parcial',
     'IA gera rascunho da folha a partir do PT6 e banco de procedimentos padrao. Auditor revisa e adapta.',
     'Media', 'Alta', 'IDs 23, 24',
     'Para cada risco Rn havera uma folha. Template + IA gera N folhas em lote.'),

    (26, 'Programacao da execucao', 4,
     'Rn - Folhas descritivas adicionais (PT7)',
     'Folhas descritivas para testes de controle e substantivos dos riscos adicionais Rn, usando PT7.',
     'PT7 Folha de teste.doc', 'Publicos internos', 'Baixa', 'Parcial',
     'Redacao/Tecnica', 'Parcial',
     'Mesma solucao do ID 25, geracao batch para todos os riscos significativos.',
     'Media', 'Alta', 'IDs 23, 24, 25',
     'Replicacao em lote amplifica o ganho de automacao.'),
]

style_rows(ws, data, center_cols=[1, 3, 7, 8, 9, 10, 11, 13, 14])

for i in range(2, len(data) + 2):
    auto = ws.cell(row=i, column=11).value
    fills = {'Alto': GREEN, 'Parcial': YELLOW, 'Baixo': RED}
    if auto in fills:
        ws.cell(row=i, column=11).fill = fills[auto]

ws.auto_filter.ref = f'A1:P{len(data)+1}'

# ── Sheet 2: Resumo Executivo ──
ws2 = wb.create_sheet('Resumo Executivo')
h2 = ['Categoria', 'Qtd', 'Alto', 'Parcial', 'Baixo', '% Automatizavel']
w2 = [35, 10, 10, 10, 10, 18]
style_header(ws2, h2, w2)

s2 = [
    ('POTENCIAL DE AUTOMACAO', '', '', '', '', ''),
    ('  Alto (>70% automatico)', 4, '', '', '', ''),
    ('  Parcial (30-70% + humano)', 16, '', '', '', ''),
    ('  Baixo (<30%, essencialmente humano)', 6, '', '', '', ''),
    ('', '', '', '', '', ''),
    ('POR TESTE', 'Qtd', 'Alto', 'Parcial', 'Baixo', '%'),
    ('Formalizacao', 3, 2, 1, 0, '=ROUND((C8+D8)/B8*100,0)'),
    ('Entendimento do objeto', 9, 1, 6, 2, '=ROUND((C9+D9)/B9*100,0)'),
    ('Identificacao de riscos', 2, 0, 2, 0, '=ROUND((C10+D10)/B10*100,0)'),
    ('Avaliacao de controles', 5, 0, 3, 2, '=ROUND((C11+D11)/B11*100,0)'),
    ('Avaliacao de riscos', 1, 0, 1, 0, '=ROUND((C12+D12)/B12*100,0)'),
    ('Objetivos especificos e escopo', 2, 0, 1, 1, '=ROUND((C13+D13)/B13*100,0)'),
    ('Programacao da execucao', 4, 1, 3, 0, '=ROUND((C14+D14)/B14*100,0)'),
    ('TOTAL', '=SUM(B8:B14)', '=SUM(C8:C14)', '=SUM(D8:D14)', '=SUM(E8:E14)', '=ROUND((C15+D15)/B15*100,0)'),
    ('', '', '', '', '', ''),
    ('SENSIBILIDADE DE DADOS', 'Qtd', '', '', '', ''),
    ('  Baixa (dados publicos)', 18, '', '', '', ''),
    ('  Media (possiveis dados pessoais/sigilosos)', 7, '', '', '', ''),
    ('  Alta (dados pessoais certos - LGPD)', 1, '', '', '', ''),
    ('', '', '', '', '', ''),
    ('DECISAO HUMANA', 'Qtd', '', '', '', ''),
    ('  Sim (obrigatoria)', 14, '', '', '', ''),
    ('  Parcial (humano valida)', 10, '', '', '', ''),
    ('  Nao (totalmente automatizavel)', 2, '', '', '', ''),
]

style_rows(ws2, s2, center_cols=[2, 3, 4, 5, 6])
for i, row in enumerate(s2, 2):
    if row[0] and row[0].isupper():
        for j in range(1, 7):
            ws2.cell(row=i, column=j).font = BOLD_FONT
    if row[0] == 'TOTAL':
        for j in range(1, 7):
            ws2.cell(row=i, column=j).fill = SUBHEADER_FILL

# ── Sheet 3: Quick Wins ──
ws3 = wb.create_sheet('Quick Wins')
h3 = ['#', 'ID', 'Passo', 'Solucao Proposta', 'Esforco', 'Impacto']
w3 = [5, 5, 35, 55, 15, 50]
style_header(ws3, h3, w3)

qw = [
    (1, 2, 'Comunicacao formal (PT0)',
     'Template parametrizado que puxa dados do Sicoi e gera PT0', '2-3 semanas',
     'Elimina trabalho manual em 100% das acoes de controle'),
    (2, 1, 'Solicitacao de informacoes',
     'Template inteligente de memorando com campos estruturados', '2-3 semanas',
     'Padroniza e acelera todas as solicitacoes iniciais'),
    (3, 24, 'Plano amostral',
     'Calculadora de amostragem integrada ao PT6', '3-4 semanas',
     'Elimina erros de calculo e documenta parametros automaticamente'),
    (4, 11, 'Marcos regulatorios',
     'Busca automatizada em bases legislativas com classificacao por IA', '1-2 meses',
     'Reduz pesquisa de normativos de dias para horas'),
    (5, 25, 'Folhas de teste (R1...Rn)',
     'Geracao em lote de PT7 a partir do PT6', '1-2 meses',
     'Para 5+ riscos, economia de dias por auditoria'),
    (6, 8, 'Diagrama de escopo',
     'IA gera rascunho integrando dados do PT1', '2-3 meses',
     'Entregavel principal; economia de 2-3 dias/auditoria'),
    (7, 18, 'Diagrama processos/riscos/controles',
     'Visualizacao interativa consolidando PT1+PT2+PT3', '3-4 meses',
     'Produto de maior valor agregado do planejamento'),
    (8, 13, 'Sugestao de riscos por IA',
     'Base de riscos por tipo de processo, alimentada por historico', '3-6 meses',
     'Acelera brainstorming e garante cobertura historica'),
]

style_rows(ws3, qw, center_cols=[1, 2, 5])
for i in range(2, len(qw) + 2):
    p = i - 1
    if p <= 3:
        ws3.cell(row=i, column=1).fill = GREEN
    elif p <= 5:
        ws3.cell(row=i, column=1).fill = YELLOW
    else:
        ws3.cell(row=i, column=1).fill = ORANGE

# ── Sheet 4: Legenda ──
ws4 = wb.create_sheet('Legenda e Criterios')
h4 = ['Campo', 'Valor', 'Descricao']
w4 = [28, 22, 80]
style_header(ws4, h4, w4)

leg = [
    ('Potencial de Automacao', 'Alto', 'Atividade pode ser >70% automatica, com validacao humana minima.'),
    ('', 'Parcial', 'IA/sistema executa 30-70%, requer complementacao humana substantiva.'),
    ('', 'Baixo', 'Essencialmente humana (<30%): reunioes, decisoes, negociacoes.'),
    ('', '', ''),
    ('Sensibilidade de Dados', 'Baixa', 'Apenas dados publicos ou internos nao sensiveis.'),
    ('', 'Media', 'Pode envolver dados pessoais ou orcamentarios com restricao de acesso.'),
    ('', 'Alta', 'Dados pessoais certos (LGPD) ou informacoes sigilosas.'),
    ('', '', ''),
    ('Decisao Humana?', 'Sim', 'Julgamento profissional ou decisao gerencial indelegavel.'),
    ('', 'Parcial', 'Sistema prepara insumos; humano valida e complementa.'),
    ('', 'Nao', 'Executavel por sistema sem intervencao humana.'),
    ('', '', ''),
    ('Natureza', 'Burocratica', 'Documentos formais, memorandos, comunicacoes padronizadas.'),
    ('', 'Analitica/Decisoria', 'Analise com julgamento profissional para decisao.'),
    ('', 'Pesquisa/Descritiva', 'Coleta e sistematizacao de informacoes.'),
    ('', 'Interacao humana', 'Reunioes, apresentacoes, negociacoes presenciais.'),
    ('', 'Sintese/Compilacao', 'Consolidacao de informacoes em formato estruturado.'),
    ('', 'Tecnica/Estatistica', 'Calculos, amostragem, metodos quantitativos.'),
    ('', 'Redacao/Tecnica', 'Elaboracao de documentos tecnicos detalhados.'),
    ('', '', ''),
    ('Complexidade', 'Baixa', 'Templates, formularios simples. Semanas.'),
    ('', 'Media', 'Integracao com sistemas, IA para texto. 1-3 meses.'),
    ('', 'Alta', 'IA avancada, multiplos sistemas, diagramacao. 3-6 meses.'),
    ('', '', ''),
    ('Prioridade', 'Alta', 'Ganho imediato, alta frequencia, baixa complexidade.'),
    ('', 'Media', 'Ganho relevante mas complexidade ou dependencias adiam.'),
    ('', 'Baixa', 'Ganho marginal ou atividade inerentemente humana.'),
]

style_rows(ws4, leg)
for i, row in enumerate(leg, 2):
    if row[0]:
        ws4.cell(row=i, column=1).font = BOLD_FONT

output = 'Roadmap_Automacao_Planejamento_Auditoria.xlsx'
wb.save(output)
print(f'Saved: {output}')
print(f'Sheets: {wb.sheetnames}')
print(f'Data rows: {len(data)}')
