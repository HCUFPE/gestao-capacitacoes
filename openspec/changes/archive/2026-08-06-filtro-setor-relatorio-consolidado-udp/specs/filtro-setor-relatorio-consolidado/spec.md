## ADDED Requirements

### Requirement: Filtragem por setor no Relatório Consolidado UDP
O sistema DEVE permitir a filtragem dos dados do Relatório Consolidado por setor/lotação na interface web do perfil UDP.

#### Scenario: Seleção de setor no filtro
- **WHEN** o usuário seleciona um setor específico no dropdown de filtro de lotações da página
- **THEN** a tabela e as estatísticas do relatório consolidado DEVEM ser atualizadas exibindo apenas os servidores e cursos pertencentes àquele setor

#### Scenario: Visualizar todos os setores
- **WHEN** o usuário seleciona a opção "Todos os Setores" ou limpa o filtro de setor
- **THEN** a tabela DEVE ser exibida com os dados consolidados de todas as lotações

### Requirement: Filtragem por setor nos endpoints de exportação
Os endpoints de exportação em Excel e PDF do Relatório Consolidado UDP DEVEM aceitar o parâmetro opcional de consulta `setor` (ou `lotacao`) para gerar relatórios filtrados.

#### Scenario: Exportação para Excel com filtro de setor
- **WHEN** uma requisição de exportação Excel é feita passando `setor=UNIDADE DE DESENVOLVIMENTO DE PESSOAL`
- **THEN** o arquivo gerado DEVE conter apenas os registros dos servidores pertencentes a essa unidade

#### Scenario: Exportação para PDF com filtro de setor
- **WHEN** uma requisição de exportação PDF é feita passando `setor=UNIDADE DE DESENVOLVIMENTO DE PESSOAL`
- **THEN** o documento PDF gerado DEVE conter apenas os registros da unidade especificada
