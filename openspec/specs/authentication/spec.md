# authentication Specification

## Purpose
TBD - created by archiving change project-specs. Update Purpose after archive.
## Requirements
### Requirement: User authenticates via Active Directory

O sistema SHALL autenticar usuários contra o Active Directory corporativo usando credenciais OAuth2 (username + password) e SHALL retornar um JWT access token válido após autenticação bem-sucedida.

#### Scenario: Successful AD authentication
- **WHEN** usuário envia credentials válidas para POST /api/login
- **THEN** sistema retorna access_token tipo bearer e token_type

#### Scenario: Failed AD authentication
- **WHEN** usuário envia credentials inválidas para POST /api/login
- **THEN** sistema retorna HTTP 401 com detail de erro

### Requirement: Access token follows JWT short-lived pattern

O sistema SHALL emitir JWT access tokens com vida curta (configurável via JWT_EXP_HOURS) e SHALL incluir no payload o username (sub), perfil, displayName, email e groups do usuário.

#### Scenario: Token contains user profile
- **WHEN** usuário autenticado recebe access token
- **THEN** token contém claims sub, perfil, displayName, email, groups

### Requirement: Refresh token is stored as HttpOnly cookie

O sistema SHALL suportar refresh de access token via refresh token armazenado em HttpOnly cookie e SHALL invalidar o refresh token antigo ao emitir um novo (token rotation).

#### Scenario: Token refresh with remember_me
- **WHEN** usuário faz login com remember_me=true
- **THEN** sistema seta cookie refresh_token HttpOnly e retorna access_token

#### Scenario: Token refresh rotation
- **WHEN** usuário chama POST /api/token/refresh com cookie válido
- **THEN** sistema invalida o token antigo, emite novo access token e novo cookie de refresh

### Requirement: Logout invalidates refresh token

O sistema SHALL invalidar o refresh token e remover o cookie HttpOnly ao usuário efetuar logout.

#### Scenario: Successful logout
- **WHEN** usuário autenticado chama POST /api/logout
- **THEN** sistema invalida refresh token no BD e remove cookie refresh_token

### Requirement: User data synchronization on login

O sistema SHALL sincronizar os dados do usuário do AD com o banco local a cada login, criando ou atualizando o registro no modelo Usuario.

#### Scenario: New user sync
- **WHEN** usuário loga pela primeira vez com credentials válidas
- **THEN** sistema cria registro Usuario no BD local com dados do AD e perfil padrão Trabalhador

#### Scenario: Existing user sync
- **WHEN** usuário já cadastrado loga novamente
- **THEN** sistema atualiza dados do AD no registro Usuario existente

### Requirement: Protected endpoints require valid JWT

O sistema SHALL rejeitar requisições em endpoints protegidos sem JWT válido no header Authorization, retornando HTTP 401.

#### Scenario: Unauthenticated request
- **WHEN** requisição chega a /api/cursos sem header Authorization
- **THEN** sistema retorna HTTP 401

### Requirement: Profile-based route guards

O sistema SHALL restringir acesso a endpoints baseado no perfil do usuário (Trabalhador, Chefia, UDP), retornando HTTP 403 quando o perfil não é suficiente.

#### Scenario: Unauthorized profile access
- **WHEN** usuário com perfil Trabalhador chama PUT /api/admin/usuarios/perfil
- **THEN** sistema retorna HTTP 403

#### Scenario: Authorized profile access
- **WHEN** usuário com perfil UDP chama PUT /api/admin/usuarios/perfil
- **THEN** sistema processa a requisição

### Requirement: Current user endpoint returns local profile data

O sistema SHALL prover um endpoint GET /api/users/me que retorna os dados do usuário logado a partir do banco local, incluindo perfil, lotação e cargo.

#### Scenario: Get current user
- **WHEN** usuário autenticado chama GET /api/users/me
- **THEN** sistema retorna username, displayName, email, perfil, department, title, employeeNumber

