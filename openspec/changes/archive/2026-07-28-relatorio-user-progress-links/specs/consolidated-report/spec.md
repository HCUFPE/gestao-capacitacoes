## ADDED Requirements

### Requirement: Consolidated report displays clickable user name

O sistema SHALL exibir o nome do profissional como link clicável na tabela do relatório consolidado (Chefia e UDP), abrindo um modal com detalhes do usuário quando clicado.

#### Scenario: User name is clickable in consolidated report
- **WHEN** Chefia ou UDP visualiza relatório consolidado
- **THEN** coluna "Nome" exibe nome como link clicável

#### Scenario: Clicking name opens user details in consolidated report
- **WHEN** Chefia ou UDP clica no nome do profissional no relatório consolidado
- **THEN** sistema abre modal com cursos, certificados e progresso do usuário

#### Scenario: Chefia permissions respected in consolidated report
- **WHEN** Chefia clica no nome de um profissional no relatório consolidado
- **THEN** sistema abre detalhes apenas se o profissional pertence à lotação da chefia
