## ADDED Requirements

### Requirement: System provides consolidated report for Mentor compliance

O sistema SHALL prover um relatório consolidado para comprovação de capacitações no sistema Mentor, acessível pela Chefia e pela UDP. O relatório deve conter: nome do profissional, curso, status, data de envio do certificado, vínculo e indicação de certificado enviado.

#### Scenario: Chefia accesses consolidated report
- **WHEN** Chefia chama GET /api/relatorios/chefia/consolidado
- **THEN** sistema retorna dados consolidados da lotação da chefia com campos: nome, curso, status, data_envio_certificado, vinculo, certificado_enviado

#### Scenario: UDP accesses consolidated report
- **WHEN** UDP chama GET /api/relatorios/udp/consolidado
- **THEN** sistema retorna dados consolidados de toda a base

#### Scenario: Consolidated report includes certificate submission date
- **WHEN** certificado foi enviado para uma atribuição
- **THEN** data_envio_certificado contém o valor de data_conclusao da Atribuicao

#### Scenario: Consolidated report shows no certificate
- **WHEN** usuário não enviou certificado para o curso
- **THEN** certificado_enviado é "Não" e data_envio_certificado é nulo

### Requirement: Consolidated report can be exported to Excel and PDF

O sistema SHALL permitir exportação do relatório consolidado em Excel (GET /api/relatorios/chefia/consolidado/export/excel) e PDF (GET /api/relatorios/chefia/consolidado/export/pdf).

#### Scenario: Export consolidated report to Excel
- **WHEN** Chefia chama GET /api/relatorios/chefia/consolidado/export/excel
- **THEN** sistema retorna arquivo .xlsx com Content-Disposition attachment

#### Scenario: Export consolidated report to PDF
- **WHEN** Chefia chama GET /api/relatorios/chefia/consolidado/export/pdf
- **THEN** sistema retorna arquivo .pdf com Content-Disposition attachment e layout legível

### Requirement: Consolidated report respects filters

O sistema SHALL aplicar filtros de ano e vínculo ao relatório consolidado.

#### Scenario: Consolidated report with year filter
- **WHEN** Chefia chama GET /api/relatorios/chefia/consolidado?ano=2025
- **THEN** sistema retorna apenas registros com data_envio_certificado em 2025

#### Scenario: Consolidated report with vinculo filter
- **WHEN** Chefia chama GET /api/relatorios/chefia/consolidado?vinculo=EBSERH
- **THEN** sistema retorna apenas registros de usuários com vinculo "EBSERH"

### Requirement: Chefia can view certificates before exporting

O sistema SHALL permitir que a chefia visualize os certificados individuais a partir do relatório consolidado, sem precisar baixar um por um.

#### Scenario: View certificate from consolidated report
- **WHEN** Chefia visualiza relatório consolidado e o registro possui certificado
- **THEN** sistema exibe botão/link "Visualizar certificado" que abre o arquivo do certificado
