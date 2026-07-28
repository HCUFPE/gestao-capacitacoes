# course-management Specification

## Purpose
TBD - created by archiving change project-specs. Update Purpose after archive.
## Requirements
### Requirement: Course model stores EAD course metadata

O sistema SHALL manter um modelo Curso com campos: id, titulo, certificadora, carga_horaria, link, tema, ano_gd, lotacao_id, atribuir_a_todos, conteudista, disponibilidade_dias, tipo_oferta, apresentacao, publico_alvo, conteudo_programatico, data_lancamento, acessibilidade, observacao, criado_em, atualizado_em.

#### Scenario: Curso has required fields
- **WHEN** registro Curso é criado
- **THEN** titulo é obrigatório; demais campos são opcionais

### Requirement: Chefia and UDP can create courses

O sistema SHALL permitir que usuários com perfil Chefia ou UDP criem novos cursos via POST /api/cursos.

#### Scenario: Create course
- **WHEN** Chefia envia POST /api/cursos com CursoCreate payload
- **THEN** sistema retorna HTTP 201 com CursoResponse

#### Scenario: Unauthorized create
- **WHEN** Trabalhador envia POST /api/cursos
- **THEN** sistema retorna HTTP 403

### Requirement: Chefia and UDP can update courses

O sistema SHALL permitir que usuários com perfil Chefia ou UDP atualizem cursos existentes via PUT /api/cursos/{curso_id}.

#### Scenario: Update existing course
- **WHEN** Chefia envia PUT /api/cursos/{id} com CursoCreate payload
- **THEN** sistema retorna CursoResponse atualizado

#### Scenario: Update non-existent course
- **WHEN** Chefia envia PUT /api/cursos/{id} com id inexistente
- **THEN** sistema retorna HTTP 404

### Requirement: Chefia and UDP can delete courses

O sistema SHALL permitir que usuários com perfil Chefia ou UDP removam cursos via DELETE /api/cursos/{curso_id}, deletando também as atribuições associadas.

#### Scenario: Delete course
- **WHEN** Chefia envia DELETE /api/cursos/{id}
- **THEN** sistema retorna HTTP 204 e remove curso e atribuições vinculadas

#### Scenario: Delete non-existent course
- **WHEN** Chefia envia DELETE /api/cursos/{id} com id inexistente
- **THEN** sistema retorna HTTP 404

### Requirement: System lists courses with pagination and filters

O sistema SHALL prover listagem paginada de cursos via GET /api/cursos com filtros opcionais por titulo e tema.

#### Scenario: Paginated course list
- **WHEN** usuário autenticado chama GET /api/cursos?skip=0&limit=10
- **THEN** sistema retorna PaginatedCursoResponse

#### Scenario: Filter by titulo
- **WHEN** usuário chama GET /api/cursos?titulo=segurança
- **THEN** sistema retorna cursos cujo título contém "segurança"

#### Scenario: Filter by tema
- **WHEN** usuário chama GET /api/cursos?tema=TI
- **THEN** sistema retorna cursos com tema "TI"

### Requirement: System provides recommended courses by user lotacao

O sistema SHALL recomendar cursos filtrados pela lotação do usuário logado, excluindo cursos em que o usuário já está inscrito ou que já foram atribuídos.

#### Scenario: Recommended courses for user
- **WHEN** usuário com lotacao definida chama GET /api/cursos/recommended
- **THEN** sistema retorna cursos da lotação do usuário excluíndo inscrições e atribuições existentes

#### Scenario: Recommended courses for user without lotacao
- **WHEN** usuário sem lotacao chama GET /api/cursos/recommended
- **THEN** sistema retorna lista vazia

### Requirement: System provides generic courses

O sistema SHALL listar cursos genéricos (sem lotação específica), excluindo os que o usuário já se inscreveu ou que já foram atribuídos.

#### Scenario: Generic courses
- **WHEN** usuário autenticado chama GET /api/cursos/genericos
- **THEN** sistema retorna cursos sem lotacao_id excluíndo inscrições e atribuições

### Requirement: System returns single course by ID

O sistema SHALL retornar os detalhes de um curso específico via GET /api/cursos/{curso_id}.

#### Scenario: Get course by ID
- **WHEN** usuário autenticado chama GET /api/cursos/{id} válido
- **THEN** sistema retorna CursoResponse

#### Scenario: Course not found
- **WHEN** usuário autenticado chama GET /api/cursos/{id} inexistente
- **THEN** sistema retorna HTTP 404

