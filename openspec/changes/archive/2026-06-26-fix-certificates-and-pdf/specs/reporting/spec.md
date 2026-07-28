## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: PDF export includes all report columns without truncation

O sistema SHALL incluir todas as colunas do relatório na exportação PDF: nome_profissional, cpf, vinculo, setor, nome_curso, plataforma, carga_horaria, ano_gd, certificado.

#### Scenario: All columns present in PDF
- **WHEN** PDF é exportado com dados completos
- **THEN** todas as colunas do relatório são visíveis e legíveis no PDF gerado

#### Scenario: vinculo column is included in PDF
- **WHEN** usuário possui vínculo cadastrado
- **THEN** o campo vinculo aparece na exportação PDF com o valor correto
