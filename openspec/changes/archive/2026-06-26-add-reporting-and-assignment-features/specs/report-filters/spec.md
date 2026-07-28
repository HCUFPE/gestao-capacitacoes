## ADDED Requirements

### Requirement: Reports can be filtered by year

O sistema SHALL permitir filtrar relatórios pela data de envio do certificado, usando o ano calendário. O filtro é aplicado via query parameter `?ano=YYYY` nos endpoints de relatório da chefia e da UDP.

#### Scenario: Filter by specific year
- **WHEN** usuário chama endpoint de relatório com ?ano=2025
- **THEN** sistema retorna apenas registros onde data_conclusao do certificado está em 2025

#### Scenario: Filter with no year parameter returns all
- **WHEN** usuário chama endpoint de relatório sem parametro ano
- **THEN** sistema retorna todos os registros sem filtro de ano

#### Scenario: Filter applies to exports
- **WHEN** usuário exporta PDF ou Excel com filtro ?ano=2025
- **THEN** arquivo exportado contém apenas dados do ano 2025

### Requirement: Reports can be filtered by vinculo

O sistema SHALL permitir filtrar relatórios por vínculo do usuário (RJU, EBSERH, etc.) via query parameter `?vinculo=X`. A opção "Todos" ou parametro ausente retorna sem filtro.

#### Scenario: Filter by specific vinculo
- **WHEN** usuário chama endpoint de relatório com ?vinculo=EBSERH
- **THEN** sistema retorna apenas registros de usuários com vinculo "EBSERH"

#### Scenario: Filter with no vinculo parameter returns all
- **WHEN** usuário chama endpoint de relatório sem parametro vinculo
- **THEN** sistema retorna todos os registros independentemente do vinculo

#### Scenario: Filter applies to exports
- **WHEN** usuário exporta PDF ou Excel com filtro ?vinculo=RJU
- **THEN** arquivo exportado contém apenas dados de usuários com vinculo "RJU"

#### Scenario: Users without vinculo
- **WHEN** filtro por vinculo é aplicado e usuário não tem vinculo cadastrado
- **THEN** usuário sem vinculo é excluído do resultado, a menos que filtro seja "Todos" ou ausente

### Requirement: Frontend provides filter UI for reports

O sistema SHALL exibir controles de filtro por ano e por vínculo nas telas de relatórios da chefia e da UDP.

#### Scenario: Year filter dropdown
- **WHEN** usuário abre tela de relatórios
- **THEN** sistema exibe dropdown de seleção de ano com anos disponíveis baseados nos dados

#### Scenario: Vinculo filter dropdown
- **WHEN** usuário abre tela de relatórios
- **THEN** sistema exibe dropdown de seleção de vínculo com opções "Todos" e os vínculos disponíveis

#### Scenario: Filters apply to table and exports
- **WHEN** usuário aplica filtros
- **THEN** tabela na tela e botões de exportação respeitam os filtros selecionados
