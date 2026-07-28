# enrollment Specification

## Purpose
TBD - created by archiving change project-specs. Update Purpose after archive.
## Requirements
### Requirement: User can self-enroll in a course

O sistema SHALL permitir que qualquer usuário autenticado se inscreva voluntariamente em um curso via POST /api/inscricoes, criando automaticamente uma inscrição e uma atribuição vinculada com status Pendente.

#### Scenario: Successful enrollment
- **WHEN** usuário autenticado envia POST /api/inscricoes com curso_id válido
- **THEN** sistema retorna HTTP 201 com InscricaoResponse contendo id, user_id, curso_id, inscrito_em, curso, atribuicao_id e status

#### Scenario: Duplicate enrollment
- **WHEN** usuário já inscrito envia POST /api/inscricoes com mesmo curso_id
- **THEN** sistema retorna HTTP 409 com detail "Usuário já inscrito neste curso"

### Requirement: User can list their enrollments

O sistema SHALL permitir que usuário autenticado liste todas as suas inscrições via GET /api/inscricoes/me, incluindo dados do curso e status da atribuição vinculada.

#### Scenario: List user enrollments
- **WHEN** usuário autenticado chama GET /api/inscricoes/me
- **THEN** sistema retorna lista de InscricaoResponse com curso, atribuicao_id, status, certificado info

### Requirement: User can withdraw from a course

O sistema SHALL permitir que usuário autenticado se desinscreva de um curso via DELETE /api/inscricoes/{inscricao_id}, desde que a inscrição pertença ao usuário logado.

#### Scenario: Successful withdrawal
- **WHEN** usuário autenticado chama DELETE /api/inscricoes/{id} da própria inscrição
- **THEN** sistema retorna HTTP 204

#### Scenario: Unauthorized withdrawal
- **WHEN** usuário chama DELETE /api/inscricoes/{id} de inscrição de outro usuário
- **THEN** sistema retorna HTTP 403

#### Scenario: Withdrawal non-existent
- **WHEN** usuário chama DELETE /api/inscricoes/{id} inexistente
- **THEN** sistema retorna HTTP 404

### Requirement: Enrollment creates linked assignment

O sistema SHALL criar automaticamente uma Atribuicao vinculada quando usuário se inscreve, com status Pendente e flag criado_por_usuario=true.

#### Scenario: Enrollment creates assignment
- **WHEN** usuário se inscreve em curso
- **THEN** sistema cria Atribuicao com user_id, curso_id, status=Pendente, criado_por_usuario=True

