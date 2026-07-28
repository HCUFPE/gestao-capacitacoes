# course-assignment Specification

## Purpose
TBD - created by archiving change project-specs. Update Purpose after archive.
## Requirements
### Requirement: Assignment model tracks course completion status

O sistema SHALL manter um modelo Atribuicao com campos: id, user_id, curso_id, status, atribuido_em, criado_por_usuario, certificado_id, data_conclusao. O status segue máquina de estados: Pendente → Em Andamento → Realizado → Concluído.

#### Scenario: Assignment status values
- **WHEN** Atribuicao é criada
- **THEN** status inicial é Pendente

#### Scenario: Assignment status progression
- **WHEN** certificado é submetido para Atribuicao
- **THEN** status muda para Realizado

#### Scenario: Assignment final status
- **WHEN** Chefia/UDP valida certificado de Atribuicao com status Realizado
- **THEN** status muda para Concluído

### Requirement: User can list their assignments

O sistema SHALL permitir que usuário autenticado liste suas atribuições via GET /api/atribuicoes/me.

#### Scenario: List user assignments
- **WHEN** usuário autenticado chama GET /api/atribuicoes/me
- **THEN** sistema retorna lista de AtribuicaoResponse com id, status, atribuido_em, curso

### Requirement: Chefia can view pending validations for their lotacao

O sistema SHALL permitir que usuários com perfil Chefia listem atribuições com certificados submetidos (status Realizado) que aguardam validação, filtradas pela lotação do usuário.

#### Scenario: Chefia views pending validations
- **WHEN** Chefia chama GET /api/atribuicoes/pendentes-validacao
- **THEN** sistema retorna lista de AtribuicaoPendenteResponse da lotação da chefia

#### Scenario: Chefia without lotacao
- **WHEN** Chefia sem lotacao chama GET /api/atribuicoes/pendentes-validacao
- **THEN** sistema retorna HTTP 400

### Requirement: Assignment is linked to certificate upon submission

O sistema SHALL atualizar a Atribuicao com certificado_id e data_conclusao quando certificado é submetido.

#### Scenario: Assignment updated with certificate
- **WHEN** certificado é submetido para uma Atribuicao
- **THEN** sistema atualiza atribuicao com certificado_id e status=Realizado

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

