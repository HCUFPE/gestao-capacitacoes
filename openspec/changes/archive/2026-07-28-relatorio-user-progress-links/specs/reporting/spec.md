## ADDED Requirements

### Requirement: Capacitacoes report displays clickable user name

O sistema SHALL exibir o nome do profissional como link clicável na tabela do relatório detalhado de capacitações (GET /api/relatorios/capacitacoes), abrindo um modal com detalhes do usuário quando clicado.

#### Scenario: User name is clickable in capacitacoes report
- **WHEN** UDP visualiza relatório de capacitações
- **THEN** coluna "Profissional" exibe nome como link clicável

#### Scenario: Clicking name opens user details
- **WHEN** UDP clica no nome do profissional
- **THEN** sistema abre modal com cursos, certificados e progresso do usuário
