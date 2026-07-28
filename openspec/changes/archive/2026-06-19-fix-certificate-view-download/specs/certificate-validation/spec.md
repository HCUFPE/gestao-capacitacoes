## MODIFIED Requirements

### Requirement: Chefia and UDP can validate or reject certificates

O sistema SHALL permitir que Chefia ou UDP validem ou rejeitem certificados submetidos via POST /api/certificados/validar, atualizando o status da Atribuicao para Concluído (validado) ou Recusado (recusado). O modelo StatusAtribuicao SHALL conter os valores: Pendente, Em Andamento, Concluído, Realizado, Validado, Recusado, com valores em Title Case consistente.

#### Scenario: Validate certificate
- **WHEN** Chefia envia POST /api/certificados/validar com atribuicao_id e status=Concluído
- **THEN** sistema atualiza status da Atribuicao para Concluído e retorna HTTP 204

#### Scenario: Reject certificate
- **WHEN** Chefia envia POST /api/certificados/validar com atribuicao_id e status=Recusado
- **THEN** sistema atualiza status da Atribuicao para Recusado e retorna HTTP 204

#### Scenario: Invalid validation status
- **WHEN** Chefia envia status inválido para POST /api/certificados/validar
- **THEN** sistema retorna HTTP 400

#### Scenario: Unauthorized validation
- **WHEN** Trabalhador envia POST /api/certificados/validar
- **THEN** sistema retorna HTTP 403

#### Scenario: Enum values are consistent Title Case
- **WHEN** StatusAtribuicao é consultado
- **THEN** todos os valores são Title Case: "Pendente", "Em Andamento", "Concluído", "Realizado", "Validado", "Recusado"

## ADDED Requirements

### Requirement: Assignment response includes certificate data

O sistema SHALL incluir dados do certificado (`certificado_id`, `certificado_file_path`, `certificado_link`) nas respostas de `/api/atribuicoes/me` quando existir um certificado vinculado à atribuição.

#### Scenario: Assignment with certificate returns certificate data
- **WHEN** usuário autenticado chama GET /api/atribuicoes/me e possui atribuição com certificado vinculado
- **THEN** resposta inclui certificado_id, certificado_file_path e/ou certificado_link na atribuição

#### Scenario: Assignment without certificate omits certificate data
- **WHEN** usuário autenticado chama GET /api/atribuicoes/me e possui atribuição sem certificado
- **THEN** resposta retorna certificado_id, certificado_file_path e certificado_link como null

### Requirement: User can download uploaded certificate file

O sistema SHALL prover endpoint GET /api/certificados/download/{file_name} que retorna o arquivo salvo localmente com headers de download adequados.

#### Scenario: Download existing certificate file
- **WHEN** usuário autenticado chama GET /api/certificados/download/{nome_arquivo} para arquivo existente
- **THEN** sistema retorna FileResponse com Content-Disposition attachment e o arquivo é baixado

#### Scenario: Download non-existent certificate file
- **WHEN** usuário autenticado chama GET /api/certificados/download/{nome_arquivo} para arquivo inexistente
- **THEN** sistema retorna HTTP 404 com detail "Certificado não encontrado"

### Requirement: Frontend displays certificate view/download button

O sistema SHALL exibir botão de visualizar/baixar certificado no modal de detalhes do curso quando existir certificado vinculado à atribuição, independentemente do status ser Realizado, Concluído ou Validado.

#### Scenario: Certificate button shown for Realizado status
- **WHEN** usuário abre detalhe de curso com status "Realizado" e certificado vinculado
- **THEN** sistema exibe botão para visualizar/baixar certificado

#### Scenario: Certificate button shown for Concluído status
- **WHEN** usuário abre detalhe de curso com status "Concluído" e certificado vinculado
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

### Requirement: Frontend handles certificate download errors

O sistema SHALL tratar erros de download de certificado de forma clara para o usuário.

#### Scenario: File not found error
- **WHEN** usuário clica para visualizar certificado e arquivo não existe no servidor
- **THEN** sistema exibe mensagem "Certificado não disponível. O arquivo pode ter sido removido."

#### Scenario: External link fails
- **WHEN** usuário clica para ver certificado por link externo e link retorna erro
- **THEN** sistema exibe mensagem "Link do certificado inacessível. Entre em contato com sua chefia."
