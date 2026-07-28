## ADDED Requirements

### Requirement: Atualização de Certificado Existente (Re-upload)
O sistema SHALL permitir que o usuário (ou gestor) faça o re-upload ou substitua o link de um certificado previamente enviado para uma atribuição/inscrição específica, sem a necessidade de desinscrever-se do curso.

#### Scenario: Substituição de arquivo por um novo arquivo
- **WHEN** o usuário seleciona a opção "Reenviar Certificado" em um curso que já possui um arquivo anexado
- **THEN** o sistema SHALL sobrescrever a referência do certificado com o novo arquivo
- **AND** o status da atribuição SHALL retornar para "Realizado" ou "Em Análise" (limpando status prévios como "Recusado" se aplicável)

#### Scenario: Substituição de link por um novo arquivo ou link
- **WHEN** o usuário seleciona a opção "Reenviar Certificado" em um curso que já possui um link anexado
- **THEN** o sistema SHALL atualizar a entrada no banco de dados para refletir o novo anexo (seja arquivo ou link)
- **AND** o sistema SHALL renderizar a interface atualizada refletindo o novo arquivo/link

### Requirement: Botão de Reenvio no Modal de Detalhes
A interface de detalhes do curso (`CourseDetailsModal.vue`) SHALL disponibilizar um controle (botão ou ação similar) para permitir o reenvio de certificados.

#### Scenario: Exibição do botão de reenvio
- **WHEN** o usuário abre os detalhes de um curso que já possui um certificado enviado
- **THEN** a interface SHALL exibir uma opção visível para "Reenviar Certificado" (ou equivalente)

#### Scenario: Status após reenvio bem sucedido
- **WHEN** o usuário submete um novo certificado com sucesso através da interface
- **THEN** a interface SHALL ser recarregada ou atualizada dinamicamente para mostrar o novo certificado
- **AND** qualquer mensagem de erro prévia relacionada à recusa do certificado original SHALL ser removida da tela
