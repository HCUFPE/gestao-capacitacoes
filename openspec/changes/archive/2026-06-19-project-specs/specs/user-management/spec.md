## ADDED Requirements

### Requirement: User model stores AD-synchronized data

O sistema SHALL manter um modelo Usuario com campos sincronizados do AD: id (sAMAccountName), nome (displayName), email, lotacao, nome_chefia, cargo (title), matricula (employeeNumber), cpf, vinculo e perfil.

#### Scenario: Usuario has required fields
- **WHEN** registro Usuario é consultado
- **THEN** registro contém id, nome, perfil como campos obrigatórios; email, lotacao, nome_chefia, cargo, matricula, cpf, vinculo como opcionais

### Requirement: User has one of three profiles

O sistema SHALL restringir o perfil do usuário a três valores: Trabalhador, Chefia ou UDP. O perfil padrão para novos usuários é Trabalhador.

#### Scenario: Default profile assignment
- **WHEN** novo usuário é criado via sync do AD
- **THEN** perfil é definido como Trabalhador

#### Scenario: Valid profile values
- **WHEN** perfil é consultado
- **THEN** valor é um de: Trabalhador, Chefia, UDP

### Requirement: UDP can update user profiles

O sistema SHALL permitir que usuários com perfil UDP atualizem o perfil de qualquer outro usuário para qualquer um dos três valores permitidos.

#### Scenario: Update user profile
- **WHEN** UDP envia PUT /api/admin/usuarios/perfil com user_id e novo_perfil
- **THEN** sistema atualiza perfil do usuário e retorna UserProfileResponse

#### Scenario: Profile update user not found
- **WHEN** UDP envia PUT /api/admin/usuarios/perfil com user_id inexistente
- **THEN** sistema retorna HTTP 404

### Requirement: UDP can list all users with pagination and filters

O sistema SHALL permitir que usuários com perfil UDP listem todos os usuários cadastrados com paginação e filtros por nome e lotação.

#### Scenario: Paginated user list
- **WHEN** UDP chama GET /api/admin/usuarios com skip e limit
- **THEN** sistema retorna PaginatedResponse com lista de UserProfileResponse

#### Scenario: Filter users by lotacao
- **WHEN** UDP chama GET /api/admin/usuarios?lotacao=SECTOR
- **THEN** sistema retorna apenas usuários da lotação especificada

#### Scenario: Filter users by nome
- **WHEN** UDP chama GET /api/admin/usuarios?nome=João
- **THEN** sistema retorna usuários cujo nome contém "João"

### Requirement: System provides unique lotacoes list

O sistema SHALL prover um endpoint GET /api/utils/lotacoes que retorna lista de todas as lotações únicas cadastradas.

#### Scenario: Get lotacoes
- **WHEN** usuário autenticado chama GET /api/utils/lotacoes
- **THEN** sistema retorna lista de strings com nomes únicos de lotações
