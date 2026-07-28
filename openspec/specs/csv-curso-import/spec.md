
### Requirement: Importação e Upsert de Cursos via upload de CSV pela API
O sistema DEVE disponibilizar um endpoint HTTP POST que aceita o envio do arquivo `capacitacao.csv` via `multipart/form-data` para importação e atualização incremental do catálogo de cursos, restrito a perfis de administração (`is_udp` ou `is_chefia`).

#### Scenario: Importação bem-sucedida de catálogo com novos cursos e atualizações (Upsert)
- **WHEN** um administrador envia um arquivo CSV no formato de `capacitacao.csv` (delimitador `;`, encoding ISO-8859-1/UTF-8) contendo 100 cursos já cadastrados e 10 novos cursos
- **THEN** o sistema processa o arquivo, insere os 10 novos cursos, atualiza os dados dos 100 cursos existentes que tiveram alterações e retorna HTTP 200 com resumo `{ novos: 10, atualizados: X, erros: 0 }`.

#### Scenario: Tentativa de importação por usuário sem autorização
- **WHEN** um usuário comum (trabalhador) tenta enviar um arquivo CSV para a rota de importação de cursos
- **THEN** o sistema bloqueia o acesso retornando HTTP 403 Forbidden.

#### Scenario: Formato de planilha com delimitador ou cabeçalhos inválidos
- **WHEN** o administrador envia um arquivo CSV sem as colunas obrigatórias (`id_curso`, `nome_curso`)
- **THEN** o sistema recusa o processamento e retorna HTTP 400 Bad Request explicitando a falha nos cabeçalhos.

### Requirement: Componente de Interface Web para Upload de Planilha de Capacitações
O sistema DEVE disponibilizar na interface web (Vue.js) um botão/modal que permite selecionar a planilha `capacitacao.csv`, enviar para o backend e visualizar os resultados do processamento em tempo real.

#### Scenario: Submissão e exibição de feedback do upload
- **WHEN** o usuário seleciona a planilha de cursos no modal e confirma o envio
- **THEN** a interface exibe feedback visual durante o envio e apresenta um relatório ao concluir com o número de cursos adicionados, atualizados e eventuais erros.
