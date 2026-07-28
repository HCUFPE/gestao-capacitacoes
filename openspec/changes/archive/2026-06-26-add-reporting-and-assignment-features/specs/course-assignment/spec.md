## ADDED Requirements

### Requirement: Chefia can create assignments for specific users in their lotacao

O sistema SHALL permitir que Chefia crie atribuições de curso para usuários específicos de sua lotação via POST /api/atribuicoes/lotacao, recebendo uma lista de user_ids.

#### Scenario: Granular assignment creation
- **WHEN** Chefia envia POST /api/atribuicoes/lotacao com curso_id e lista de user_ids válidos da própria lotacao
- **THEN** sistema cria Atribuicao para cada user_id com status Pendente e retorna HTTP 201

#### Scenario: User outside lotacao rejected
- **WHEN** Chefia tenta atribuir curso a usuário de outra lotacao
- **THEN** sistema retorna HTTP 403

#### Scenario: Duplicate assignment handled
- **WHEN** Chefia tenta atribuir curso já atribuído a algum usuário da lista
- **THEN** sistema ignora a duplicação ou retorna aviso sem erro fatal
