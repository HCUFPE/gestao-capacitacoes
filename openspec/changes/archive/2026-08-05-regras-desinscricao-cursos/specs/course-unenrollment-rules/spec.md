## ADDED Requirements

### Requirement: Visibilidade do Botão de Desinscrição no Frontend
A interface do usuário SHALL exibir o botão "Desinscrever-se" unicamente para cursos/inscrições com status "Em Andamento".

#### Scenario: Botão visível para status Em Andamento
- **WHEN** a inscrição do usuário possui o status "Em Andamento" (sem certificado)
- **THEN** o botão "Desinscrever-se" DEVE ser exibido na interface no card do curso.

#### Scenario: Botão oculto após envio de certificado
- **WHEN** o usuário faz o upload do certificado e o status transiciona para "Realizado", "Concluído" ou "Validado"
- **THEN** o botão "Desinscrever-se" DEVE desaparecer completamente da interface.

### Requirement: Validação de Segurança de Desinscrição no Backend
O endpoint da API `DELETE /api/inscricoes/{id}` SHALL recusar qualquer tentativa de desinscrição de registros que já possuam certificado associado.

#### Scenario: Desinscrição recusada no backend para cursos com certificado
- **WHEN** uma requisição de desinscrição for enviada para uma atribuição/inscrição com `certificado_id` preenchido
- **THEN** a API DEVE responder com código `400 Bad Request` e mensagem detalhando a impossibilidade de exclusão.
