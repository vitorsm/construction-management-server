from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Cronograma"

ws.append(["Etapa","Subetapa","Tarefa","Data de início","Data de fim"])

# Full list based on document
data = [
# Pré-Obra
("Pré-Obra","Licenças e documentação","Levantamento cadastral do imóvel","",""),
("Pré-Obra","Licenças e documentação","Contratação de responsável técnico","",""),
("Pré-Obra","Licenças e documentação","Elaboração e aprovação de projetos","",""),
("Pré-Obra","Licenças e documentação","Obtenção do alvará de construção","",""),
("Pré-Obra","Licenças e documentação","ART/RRT de projeto e execução","",""),
("Pré-Obra","Planejamento e orçamento","Estudo topográfico","",""),
("Pré-Obra","Planejamento e orçamento","Sondagem do solo","",""),
("Pré-Obra","Planejamento e orçamento","Memorial descritivo","",""),
("Pré-Obra","Planejamento e orçamento","Orçamento detalhado","",""),
("Pré-Obra","Planejamento e orçamento","Cronograma físico-financeiro preliminar","",""),
("Pré-Obra","Contratações e logística","Seleção de empreiteira","",""),
("Pré-Obra","Contratações e logística","Contratação de mão de obra","",""),
("Pré-Obra","Contratações e logística","Contratação de fornecedores","",""),
("Pré-Obra","Contratações e logística","Planejamento de recebimento de materiais","",""),
("Pré-Obra","Preparação do terreno","Limpeza do terreno","",""),
("Pré-Obra","Preparação do terreno","Demarcação da obra","",""),
("Pré-Obra","Preparação do terreno","Nivelamento preliminar","",""),

# Fundação
("Fundação","Projeto e sondagem","Interpretação do relatório de sondagem","",""),
("Fundação","Projeto e sondagem","Definição do tipo de fundação","",""),
("Fundação","Escavações","Marcação das locações","",""),
("Fundação","Escavações","Escavação de sapatas/valas","",""),
("Fundação","Concretagem","Montagem de formas","",""),
("Fundação","Concretagem","Armação de ferragens","",""),
("Fundação","Concretagem","Concretagem das fundações","",""),
("Fundação","Drenagem e proteção","Impermeabilização das fundações","",""),
("Fundação","Drenagem e proteção","Aterro e compactação","",""),

# Estrutura
("Estrutura","Pilares e vigas","Montagem de formas","",""),
("Estrutura","Pilares e vigas","Armação","",""),
("Estrutura","Pilares e vigas","Concretagem","",""),
("Estrutura","Lajes","Montagem de escoramento","",""),
("Estrutura","Lajes","Armação da laje","",""),
("Estrutura","Lajes","Concretagem da laje","",""),
("Estrutura","Escadas","Montagem e concretagem de escadas","",""),

# Alvenaria
("Alvenaria","Preparação","Instalação de vergas e contra-marcos","",""),
("Alvenaria","Assentamento","Assentamento de blocos/tijolos","",""),
("Alvenaria","Vedações","Execução de vedações internas","",""),
("Alvenaria","Vedações","Execução de vedações externas","",""),
("Alvenaria","Reforços","Execução de vergas e lintéis","",""),

# Cobertura
("Cobertura","Estrutura","Montagem da estrutura do telhado","",""),
("Cobertura","Subcobertura","Instalação de manta/subcobertura","",""),
("Cobertura","Telhas","Assentamento de telhas","",""),
("Cobertura","Calhas","Instalação de calhas e condutores","",""),
("Cobertura","Impermeabilização","Impermeabilização de platibandas","",""),

# Hidráulica
("Hidráulica","Planejamento","Dimensionamento de tubulações","",""),
("Hidráulica","Tubulações","Instalação de água fria","",""),
("Hidráulica","Tubulações","Instalação de esgoto","",""),
("Hidráulica","Tubulações","Instalação de águas pluviais","",""),
("Hidráulica","Testes","Teste de estanqueidade","",""),

# Elétrica
("Elétrica","Planejamento","Definição de cargas e circuitos","",""),
("Elétrica","Eletrodutos","Instalação de eletrodutos","",""),
("Elétrica","Cabeamento","Passagem de cabos","",""),
("Elétrica","Quadro elétrico","Montagem do quadro de distribuição","",""),
("Elétrica","Testes","Teste de continuidade e aterramento","",""),

# Esquadrias
("Esquadrias","Aquisição","Medição e pedido de esquadrias","",""),
("Esquadrias","Instalação","Instalação de portas","",""),
("Esquadrias","Instalação","Instalação de janelas","",""),
("Esquadrias","Acabamento","Selagem e calafetagem","",""),

# Revestimentos
("Revestimentos","Preparação","Chapisco/Emboço/Reboco","",""),
("Revestimentos","Pisos","Assentamento de pisos","",""),
("Revestimentos","Paredes","Assentamento de azulejos/cerâmicas","",""),
("Revestimentos","Rejuntamento","Rejuntamento de pisos e paredes","",""),

# Pintura
("Pintura","Preparação","Lixamento e massa corrida","",""),
("Pintura","Interna","Pintura interna","",""),
("Pintura","Externa","Pintura externa","",""),

# Acabamentos
("Acabamentos","Louças e metais","Instalação de vasos, torneiras e duchas","",""),
("Acabamentos","Iluminação","Instalação de luminárias","",""),
("Acabamentos","Marcenaria","Instalação de armários e bancadas","",""),

# Limpeza
("Limpeza","Limpeza pesada","Limpeza pós-obra","",""),
("Limpeza","Limpeza fina","Limpeza detalhada e vidros","",""),

# Pós-obra
("Pós-obra","Vistorias","Vistoria final","",""),
("Pós-obra","Correções","Correção de pendências","",""),
("Pós-obra","Documentação","Entrega de manuais e garantias","",""),
]

for row in data:
    ws.append(row)

filepath = "/mnt/data/cronograma_obra_completo.xlsx"
wb.save(filepath)

filepath
