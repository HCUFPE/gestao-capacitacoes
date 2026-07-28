## ADDED Requirements

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
