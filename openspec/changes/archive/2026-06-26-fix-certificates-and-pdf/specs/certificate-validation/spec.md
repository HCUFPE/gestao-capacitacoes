## MODIFIED Requirements

### Requirement: Frontend displays certificate view/download button

O sistema SHALL exibir botão de visualizar/baixar certificado no modal de detalhes do curso quando existir certificado vinculado à atribuição, independentemente do status ser Realizado, Concluído ou Validado.

#### Scenario: Certificate button shown for Realizado status
- **WHEN** usuário abre detalhe de curso com status "Realizado" e certificado vinculado
- **THEN** sistema exibe botão para visualizar/baixar certificado

#### Scenario: Certificate button shown for Concluído status
- **WHEN** usuário abre detalhe de curso com status "Concluído" e certificado vinculado
- **THEN** sistema exibe botão para visualizar/baixar certificado

#### Scenario: Certificate button shown for Validado status
- **WHEN** usuário abre detalhe de curso com status "Validado" e certificado vinculado
- **THEN** sistema exibe botão para visualizar/baixar certificado

#### Scenario: Certificate button for PDF file
- **WHEN** certificado é arquivo PDF
- **THEN** botão exibe "Baixar Certificado" com ícone de download

#### Scenario: Certificate button for external link
- **WHEN** certificado é link externo
- **THEN** botão exibe "Ver Certificado Online" com ícone de globo e abre link em nova aba

#### Scenario: No button without certificate
- **WHEN** usuário abre detalhe de curso sem certificado vinculado
- **THEN** sistema não exibe botão de certificado

## ADDED Requirements

### Requirement: Certificate data is correctly passed to CourseDetailsModal from MeusCursos

O sistema SHALL garantir que os dados do certificado (`certificado_id`, `certificado_file_path`, `certificado_link`) sejam corretamente extraídos tanto de inscrições quanto de atribuições e passados ao CourseDetailsModal.

#### Scenario: Certificate data from enrollment item
- **WHEN** usuário clica em "Ver Detalhes" a partir de uma inscrição com certificado
- **THEN** CourseDetailsModal recebe certificado_file_path e/ou certificado_link corretamente

#### Scenario: Certificate data from assignment item
- **WHEN** usuário clica em "Ver Detalhes" a partir de uma atribuição com certificado
- **THEN** CourseDetailsModal recebe certificado_file_path e/ou certificado_link corretamente
