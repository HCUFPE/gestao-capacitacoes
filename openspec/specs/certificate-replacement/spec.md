# certificate-replacement Specification

## Purpose
Define requirements for certificate replacement, allowing users to re-upload and substitute already submitted certificates without losing enrollment or assignment data.

## Requirements
### Requirement: User can replace an already submitted certificate

O sistema SHALL permitir que um usuário autenticado reenvie/substitua um certificado já submetido para um curso, sem perder a inscrição ou a atribuição associada.

#### Scenario: User re-uploads certificate for course with existing certificate
- **WHEN** usuário com certificado já enviado (status Realizado/Validado/Concluído) faz upload de novo certificado via POST /api/certificados/upload
- **THEN** sistema cria novo Certificado, atualiza Atribuicao.certificado_id para o novo certificado, preserva a Inscricao e retorna HTTP 201

#### Scenario: Enrollment is preserved after certificate replacement
- **WHEN** usuário substitui certificado de um curso onde está inscrito
- **THEN** a Inscricao do usuário no curso permanece inalterada (mesmo id, mesmo inscrito_em)

#### Scenario: Only latest certificate is considered active
- **WHEN** usuário possui múltiplos certificados para o mesmo curso (substituições anteriores)
- **THEN** apenas o certificado apontado por Atribuicao.certificado_id é retornado como ativo nas respostas de API

### Requirement: Frontend shows re-upload button for courses with existing certificate

O sistema SHALL exibir um botão "Reenviar certificado" ou "Substituir certificado" no modal de detalhes do curso e nos cards de Meus Cursos quando o usuário já possui certificado enviado para o curso.

#### Scenario: Re-upload button shown in CourseDetailsModal
- **WHEN** usuário abre o modal de detalhes de um curso com status Realizado, Validado ou Concluído
- **THEN** sistema exibe botão "Reenviar certificado" ao lado ou abaixo do botão de visualizar certificado

#### Scenario: Re-upload button shown in MeusCursos card
- **WHEN** usuário visualiza a lista de cursos inscritos e o curso possui certificado enviado
- **THEN** sistema exibe opção de reenviar certificado no card ou no modal de detalhes

#### Scenario: Re-upload button not shown for courses without certificate
- **WHEN** usuário abre modal de detalhes de curso sem certificado (status Pendente ou Em Andamento)
- **THEN** sistema exibe botão "Enviar certificado" (comportamento normal, sem botão de reenvio separado)

### Requirement: Frontend distinguishes initial upload from replacement

O sistema SHALL diferenciar visualmente o upload inicial do reenvio de certificado, informando o usuário apropriadamente.

#### Scenario: Success message for replacement
- **WHEN** usuário reenvia certificado com sucesso
- **THEN** sistema exibe mensagem "Certificado substituído com sucesso!"

#### Scenario: Success message for initial upload
- **WHEN** usuário envia certificado pela primeira vez
- **THEN** sistema exibe mensagem "Certificado enviado com sucesso!"
