## ADDED Requirements

### Requirement: User can upload certificate as file

O sistema SHALL permitir que usuário autenticado faça upload de certificado em formato de arquivo (PDF) via POST /api/certificados/upload, associando-o a uma atribuição existente.

#### Scenario: Upload certificate file
- **WHEN** usuário envia POST /api/certificados/upload com arquivo e atribuicao_id
- **THEN** sistema salva arquivo em /uploads, cria Certificado com file_path, retorna HTTP 201

#### Scenario: Upload for non-existent assignment
- **WHEN** usuário envia upload com atribuicao_id inexistente
- **THEN** sistema retorna HTTP 404

### Requirement: User can register certificate via external link

O sistema SHALL permitir que usuário autenticado registre certificado via link externo via POST /api/certificados/link, associando-o a uma atribuição.

#### Scenario: Register certificate link
- **WHEN** usuário envia POST /api/certificados/link com link e atribuicao_id
- **THEN** sistema cria Certificado com link, retorna CertificadoResponse

### Requirement: Certificate submission updates assignment status

O sistema SHALL atualizar automaticamente a Atribuicao vinculada com certificado_id e status=Realizado ao registrar certificado (upload ou link).

#### Scenario: Assignment status on certificate registration
- **WHEN** certificado é registrado (arquivo ou link)
- **THEN** sistema atualiza Atribuicao: certificado_id=setado, status=Realizado

### Requirement: Chefia and UDP can validate or reject certificates

O sistema SHALL permitir que Chefia ou UDP validem ou rejeitem certificados submetidos via POST /api/certificados/validar, atualizando o status da Atribuicao para Concluído (validado) ou recuando (recusado).

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

### Requirement: User can retrieve certificate details

O sistema SHALL prover GET /api/certificados/{certificado_id} para retornar detalhes de um certificado específico.

#### Scenario: Get certificate
- **WHEN** usuário autenticado chama GET /api/certificados/{id} válido
- **THEN** sistema retorna CertificadoResponse com id, file_path, link, validado

#### Scenario: Certificate not found
- **WHEN** usuário chama GET /api/certificados/{id} inexistente
- **THEN** sistema retorna HTTP 404

### Requirement: Certificate model stores file or link

O sistema SHALL manter modelo Certificado com campos: id, curso_id (FK), file_path (opcional), link (opcional), validado (boolean, default=false).

#### Scenario: Certificate with file
- **WHEN** certificado é criado via upload
- **THEN** file_path é setado, link é nulo

#### Scenario: Certificate with link
- **WHEN** certificado é criado via link
- **THEN** link é setado, file_path é nulo
