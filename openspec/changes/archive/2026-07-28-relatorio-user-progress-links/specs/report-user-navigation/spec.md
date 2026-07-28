## ADDED Requirements

### Requirement: System provides user details endpoint accessible by authorized profiles

O sistema SHALL prover um endpoint GET /api/relatorios/usuario/{user_id}/detalhes que retorna os cursos, status e certificados de um usuário específico. O endpoint SHALL validar permissões: Chefia pode acessar apenas usuários da própria lotação; UDP pode acessar qualquer usuário.

#### Scenario: UDP accesses any user details
- **WHEN** UDP chama GET /api/relatorios/usuario/{user_id}/detalhes
- **THEN** sistema retorna lista de cursos com status e certificados do usuário

#### Scenario: Chefia accesses subordinate details
- **WHEN** Chefia chama GET /api/relatorios/usuario/{user_id}/detalhes para usuário da mesma lotação
- **THEN** sistema retorna lista de cursos com status e certificados do usuário

#### Scenario: Chefia cannot access user from different lotacao
- **WHEN** Chefia chama GET /api/relatorios/usuario/{user_id}/detalhes para usuário de outra lotação
- **THEN** sistema retorna HTTP 403

#### Scenario: Non-authorized user cannot access details
- **WHEN** usuário com perfil Trabalhador chama GET /api/relatorios/usuario/{user_id}/detalhes
- **THEN** sistema retorna HTTP 403

#### Scenario: User not found
- **WHEN** qualquer usuário autorizado chama GET /api/relatorios/usuario/{user_id}/detalhes com ID inexistente
- **THEN** sistema retorna HTTP 404

### Requirement: Report tables display clickable user name links

O sistema SHALL exibir o nome do profissional como link clicável nas tabelas dos relatórios de Capacitações (UDP) e do Relatório Consolidado (Chefia e UDP), abrindo um modal com detalhes do usuário.

#### Scenario: Clicking user name in capacitacoes report opens modal
- **WHEN** UDP clica no nome de um profissional no relatório de Capacitações
- **THEN** sistema abre modal com cursos, status e certificados desse usuário

#### Scenario: Clicking user name in consolidated report opens modal
- **WHEN** Chefia ou UDP clica no nome de um profissional no relatório Consolidado
- **THEN** sistema abre modal com cursos, status e certificados desse usuário

#### Scenario: User details modal shows loading state
- **WHEN** modal de detalhes é aberto
- **THEN** sistema exibe indicador de carregamento enquanto busca dados

#### Scenario: User details modal handles errors gracefully
- **WHEN** falha ao carregar detalhes do usuário
- **THEN** sistema exibe mensagem de erro no modal e permite fechar
