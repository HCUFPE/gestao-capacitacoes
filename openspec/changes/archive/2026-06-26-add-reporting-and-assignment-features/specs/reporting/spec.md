## ADDED Requirements

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

O sistema SHALL incluir a coluna "Vínculo" nos relatórios da UDP e nas exportações correspondentes, caso ainda não esteja presente.

#### Scenario: Vinculo shown in UDP detailed report
- **WHEN** UDP visualiza relatório detalhado de capacitações
- **THEN** coluna "Vínculo" aparece na tabela com o valor do vinculo do usuário
