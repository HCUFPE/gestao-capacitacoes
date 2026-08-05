## ADDED Requirements

### Requirement: Importação de usuários via upload de CSV pela API
O sistema DEVE disponibilizar um endpoint HTTP POST que aceita o envio de arquivo CSV via `multipart/form-data` para importação e atualização em lote de usuários no banco de dados, restrito aos administradores (`is_udp`).

#### Scenario: Importação de CSV válida executada por Administrador
- **WHEN** um administrador envia um arquivo CSV válido contendo novos usuários e usuários existentes com campos atualizados
- **THEN** o sistema processa o arquivo, insere novos usuários, atualiza dados de usuários existentes e retorna status 200 com o quantitativo de cadastrados, atualizados e erros.

#### Scenario: Tentativa de importação por usuário sem privilégio de Administrador
- **WHEN** um usuário não administrador tenta enviar um arquivo CSV para a rota de importação
- **THEN** o sistema recusa a requisição retornando status HTTP 403 Forbidden.

#### Scenario: Envio de arquivo inválido ou malformatado
- **WHEN** o administrador envia um arquivo que não seja CSV ou um CSV com colunas essenciais ausentes
- **THEN** o sistema retorna status HTTP 400 Bad Request descrevendo a falha na estrutura do arquivo.

### Requirement: Interface gráfica para upload de CSV e feedback de importação
O sistema DEVE fornecer um componente/modal na área administrativa da interface web (Vue.js) permitindo ao usuário selecionar o arquivo CSV, submetê-lo e visualizar o relatório de importação (sucessos, atualizações e falhas).

#### Scenario: Modal de importação com exibição de resultado
- **WHEN** o administrador seleciona um arquivo CSV e clica em "Importar" no modal
- **THEN** a interface exibe indicador de carregamento e, ao concluir, mostra um resumo com total de novos cadastros, atualizações e possíveis erros por linha.
