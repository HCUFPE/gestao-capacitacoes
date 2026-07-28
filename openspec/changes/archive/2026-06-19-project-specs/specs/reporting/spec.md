## ADDED Requirements

### Requirement: UDP can view full EAD training report

O sistema SHALL prover um relatório completo de capacitações EAD via GET /api/relatorios/capacitacoes, acessível apenas por usuários com perfil UDP, agregando dados de cursos, inscrições, atribuições e certificados.

#### Scenario: UDP access report
- **WHEN** UDP chama GET /api/relatorios/capacitacoes
- **THEN** sistema retorna lista completa de dados de capacitações

#### Scenario: Unauthorized report access
- **WHEN** usuário não-UDP chama GET /api/relatorios/capacitacoes
- **THEN** sistema retorna HTTP 403

### Requirement: UDP can export reports to Excel and PDF

O sistema SHALL permitir exportação do relatório de capacitações em formato Excel (GET /api/relatorios/capacitacoes/export/excel) e PDF (GET /api/relatorios/capacitacoes/export/pdf), retornando StreamingResponse com headers de download.

#### Scenario: Export Excel
- **WHEN** UDP chama GET /api/relatorios/capacitacoes/export/excel
- **THEN** sistema retorna arquivo .xlsx com Content-Disposition attachment

#### Scenario: Export PDF
- **WHEN** UDP chama GET /api/relatorios/capacitacoes/export/pdf
- **THEN** sistema retorna arquivo .pdf com Content-Disposition attachment

### Requirement: UDP can view most popular courses report

O sistema SHALL prover relatório dos cursos mais inscritos/atribuídos via GET /api/relatorios/udp/cursos-populares, limitado a N cursos (default 10).

#### Scenario: Popular courses report
- **WHEN** UDP chama GET /api/relatorios/udp/cursos-populares?limit=5
- **THEN** sistema retorna top 5 cursos mais inscritos/atribuídos

### Requirement: UDP can view overall training status report

O sistema SHALL prover relatório de status geral das capacitações via GET /api/relatorios/udp/status-geral.

#### Scenario: Overall status report
- **WHEN** UDP chama GET /api/relatorios/udp/status-geral
- **THEN** sistema retorna lista com status agregado de todas as capacitações

### Requirement: UDP can view compliance by lotacao report

O sistema SHALL prover relatório de conformidade por lotação via GET /api/relatorios/udp/conformidade-lotacao.

#### Scenario: Compliance report
- **WHEN** UDP chama GET /api/relatorios/udp/conformidade-lotacao
- **THEN** sistema retorna lista de conformidade agrupada por lotação

### Requirement: UDP can view pending certificates report

O sistema SHALL prover relatório de certificados pendentes de validação via GET /api/relatorios/udp/certificados-pendentes.

#### Scenario: Pending certificates report
- **WHEN** UDP chama GET /api/relatorios/udp/certificados-pendentes
- **THEN** sistema retorna lista de certificados com status Realizado aguardando validação

### Requirement: UDP can view users by profile and lotacao report

O sistema SHALL prover relatório de usuários agrupados por perfil e lotação via GET /api/relatorios/udp/usuarios-perfil-lotacao.

#### Scenario: Users by profile report
- **WHEN** UDP chama GET /api/relatorios/udp/usuarios-perfil-lotacao
- **THEN** sistema retorna lista de usuários agrupados por perfil e lotação

### Requirement: Chefia can view lotacao status report

O sistema SHALL prover relatório de status de cursos da própria lotação para Chefia via GET /api/relatorios/chefia/status-lotacao.

#### Scenario: Chefia lotacao status
- **WHEN** Chefia chama GET /api/relatorios/chefia/status-lotacao
- **THEN** sistema retorna status de cursos da lotação da chefia

#### Scenario: Chefia without lotacao
- **WHEN** Chefia sem lotacao chama GET /api/relatorios/chefia/status-lotacao
- **THEN** sistema retorna HTTP 400

### Requirement: Chefia can view individual progress report

O sistema SHALL prover relatório de progresso individual de subordinados para Chefia via GET /api/relatorios/chefia/progresso-individual.

#### Scenario: Individual progress report
- **WHEN** Chefia chama GET /api/relatorios/chefia/progresso-individual
- **THEN** sistema retorna progresso de cada subordinado da lotação

### Requirement: Chefia can view pending certificates for their lotacao

O sistema SHALL prover relatório de certificados pendentes de validação da própria lotação para Chefia via GET /api/relatorios/chefia/certificados-pendentes.

#### Scenario: Chefia pending certificates
- **WHEN** Chefia chama GET /api/relatorios/chefia/certificados-pendentes
- **THEN** sistema retorna certificados pendentes da lotação da chefia

### Requirement: System provides dashboard statistics

O sistema SHALL prover stats gerais do dashboard via GET /api/utils/stats, incluindo total_cursos, total_inscricoes, total_certificados_validados, total_usuarios.

#### Scenario: Dashboard stats
- **WHEN** usuário autenticado chama GET /api/utils/stats
- **THEN** sistema retorna DashboardStatsResponse com contadores agregados
