## ADDED Requirements

### Requirement: Chefia can assign a course to specific team members

O sistema SHALL permitir que um usuário com perfil Chefia selecione um curso e escolha pessoas específicas de sua equipe (lotacao) para receberem a atribuição, via POST /api/atribuicoes/lotacao.

#### Scenario: Chefia assigns course to selected users
- **WHEN** Chefia envia POST /api/atribuicoes/lotacao com curso_id e lista de user_ids da própria lotacao
- **THEN** sistema cria Atribuicao para cada user_id selecionado com status Pendente e retorna HTTP 201

#### Scenario: Chefia cannot assign to users outside their lotacao
- **WHEN** Chefia envia POST /api/atribuicoes/lotacao com user_id de outro setor
- **THEN** sistema retorna HTTP 403 com detail informando que o usuário não pertence à lotação da chefia

#### Scenario: Chefia without lotacao cannot assign
- **WHEN** Chefia sem lotacao definida envia POST /api/atribuicoes/lotacao
- **THEN** sistema retorna HTTP 400

#### Scenario: Non-existent course rejected
- **WHEN** Chefia envia POST /api/atribuicoes/lotacao com curso_id inexistente
- **THEN** sistema retorna HTTP 404

#### Scenario: Duplicate assignment prevented
- **WHEN** Chefia tenta atribuir curso que já foi atribuído a um usuário
- **THEN** sistema ignora o usuário já atribuído ou retorna HTTP 409 para aquele user_id

### Requirement: Frontend provides granular assignment UI

O sistema SHALL prover interface na tela de gestão de cursos onde a chefia pode selecionar um curso e escolher pessoas específicas da equipe para atribuição.

#### Scenario: Chefia selects course and users
- **WHEN** Chefia abre a tela de atribuição de cursos
- **THEN** sistema exibe selector de curso e lista de usuários da lotação com checkboxes

#### Scenario: Only unassigned users shown
- **WHEN** Chefia seleciona um curso para atribuir
- **THEN** sistema mostra apenas usuários da lotação que ainda não possuem o curso atribuído ou inscrito

#### Scenario: Both bulk and granular options available
- **WHEN** Chefia atribui curso
- **THEN** sistema oferece opção de atribuir para toda a equipe OU apenas para selecionados
