# reporting Specification

## Purpose
TBD - created by archiving change project-specs. Update Purpose after archive.
## Requirements
### Requirement: UDP can view full EAD training report

O sistema SHALL prover um relatório completo de capacitações EAD via GET /api/relatorios/capacitacoes, acessível apenas por usuários com perfil UDP, agregando dados de cursos, inscrições, atribuições e certificados.

#### Scenario: UDP access report
- **WHEN** UDP chama GET /api/relatorios/capacitacoes
- **THEN** sistema retorna lista completa de dados de capacitações

#### Scenario: Unauthorized report access
- **WHEN** usuário não-UDP chama GET /api/relatorios/capacitacoes
- **THEN** sistema retorna HTTP 403

### Requirement: UDP can export reports to Excel and PDF

O sistema SHALL permitir exportação do relatório de capacitações em formato Excel (GET /api/relatorios/capacitacoes/export/excel) e PDF (GET /api/relatorios/capacitacoes/export/pdf), retornando StreamingResponse com headers de download. O PDF SHALL usar layout com larguras de coluna adequadas, margens corretas, quebra de texto e paginação que garantam que nenhum campo seja cortado.

#### Scenario: Export Excel
- **WHEN** UDP chama GET /api/relatorios/capacitacoes/export/excel
- **THEN** sistema retorna arquivo .xlsx com Content-Disposition attachment

#### Scenario: Export PDF
- **WHEN** UDP chama GET /api/relatorios/capacitacoes/export/pdf
- **THEN** sistema retorna arquivo .pdf com Content-Disposition attachment

#### Scenario: PDF does not truncate long field values
- **WHEN** relatório contém valores longos em campos como nome_profissional, nome_curso ou cpf
- **THEN** PDF exibe o conteúdo completo sem cortes, usando quebra de linha automática ou ajuste de largura de coluna

#### Scenario: PDF respects page boundaries
- **WHEN** relatório possui muitos registros
- **THEN** PDF quebra páginas corretamente, sem cortar linhas ao meio e repetindo cabeçalhos se aplicável

#### Scenario: PDF column widths are proportional
- **WHEN** PDF é gerado
- **THEN** colunas de texto longo (nome, curso) recebem largura maior que colunas curtas (CH, ano GD), totalizando a largura da página

### Requirement: PDF export includes all report columns without truncation

O sistema SHALL incluir todas as colunas do relatório na exportação PDF: nome_profissional, cpf, vinculo, setor, nome_curso, plataforma, carga_horaria, ano_gd, certificado.

#### Scenario: All columns present in PDF
- **WHEN** PDF é exportado com dados completos
- **THEN** todas as colunas do relatório são visíveis e legíveis no PDF gerado

#### Scenario: Vinculo column is included in PDF
- **WHEN** usuário possui vínculo cadastrado
- **THEN** o campo vinculo aparece na exportação PDF com o valor correto

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

### Requirement: Individual progress report includes certificate view links

O sistema SHALL incluir, para cada linha do relatório de progresso individual da chefia, informações de certificado e botão/link para visualizá-lo quando disponível.

#### Scenario: Certificate view link shown when certificate exists
- **WHEN** Chefia visualiza relatório de progresso individual e subordinado possui certificado enviado
- **THEN** sistema exibe botão/link "Visualizar certificado" na linha do subordinado

#### Scenario: No certificate link shown when no certificate
- **WHEN** Chefia visualiza relatório e subordinado não possui certificado
- **THEN** sistema não exibe botão de certificado, mostrando apenas status

#### Scenario: Latest certificate is shown
- **WHEN** subordinado possui múltiplas substituições de certificado
- **THEN** sistema mostra sempre o certificado mais recente (maior data_conclusao)

### Requirement: Individual progress report includes link to user details

O sistema SHALL prover link clicável no nome do usuário no relatório de progresso individual, levando à visualização detalhada dos cursos, certificados e progresso desse subordinado.

#### Scenario: User name is clickable
- **WHEN** Chefia visualiza relatório de progresso individual
- **THEN** nome do subordinado é link clicável

#### Scenario: Clicking user name opens details
- **WHEN** Chefia clica no nome do subordinado
- **THEN** sistema abre detalhe do usuário com seus cursos, status e certificados

#### Scenario: Permissions respected
- **WHEN** Chefia acessa detalhe de subordinado
- **THEN** sistema verifica que o subordinado pertence à lotação da chefia

### Requirement: Vinculo column included in chefia reports

O sistema SHALL incluir a coluna "Vínculo" nos relatórios da chefia (status da lotação, progresso individual) e nas exportações correspondentes.

#### Scenario: Vinculo shown in progress report
- **WHEN** Chefia visualiza progresso individual
- **THEN** coluna "Vínculo" aparece na tabela com o valor do vinculo do usuário

#### Scenario: Empty vinculo displayed as "Não informado"
- **WHEN** usuário não possui vinculo cadastrado
- **THEN** sistema exibe "Não informado" na coluna de vinculo

#### Scenario: Vinculo included in exports
- **WHEN** Chefia exporta relatório
- **THEN** arquivo exportado inclui coluna de vinculo

### Requirement: Vinculo column included in UDP reports

O sistema SHALL incluir a coluna "Vínculo" nos relatórios da UDP e nas exportações correspondentes.

#### Scenario: Vinculo shown in UDP detailed report
- **WHEN** UDP visualiza relatório detalhado de capacitações
- **THEN** coluna "Vínculo" aparece na tabela com o valor do vinculo do usuário


### Requirement: Capacitacoes report displays clickable user name

O sistema SHALL exibir o nome do profissional como link clicável na tabela do relatório detalhado de capacitações (GET /api/relatorios/capacitacoes), abrindo um modal com detalhes do usuário quando clicado.

#### Scenario: User name is clickable in capacitacoes report
- **WHEN** UDP visualiza relatório de capacitações
- **THEN** coluna "Profissional" exibe nome como link clicável

#### Scenario: Clicking name opens user details
- **WHEN** UDP clica no nome do profissional
- **THEN** sistema abre modal com cursos, certificados e progresso do usuário
