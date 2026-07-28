## Context

Atualmente, o fluxo de envio de certificados é de "caminho único" (one-way). Ao enviar um certificado via arquivo (`/api/certificados/upload`) ou link (`/api/certificados/link`), o sistema vincula o certificado à `Atribuicao` do usuário. Se o usuário enviar um arquivo errado e perceber o erro, ou se a chefia recusar o certificado e mudar o status de volta para um estado onde se espera uma ação, o usuário não tem como sobrescrever ou reenviar outro certificado; ele precisa se desinscrever do curso e reinscrever, o que é prejudicial para a usabilidade.

## Goals / Non-Goals

**Goals:**
- Permitir a sobrescrita do arquivo ou link do certificado em uma `Atribuicao` existente.
- Garantir que a sobrescrita de arquivo remova (ou não cause vazamento de armazenamento) do arquivo antigo.
- Resetar o status da atribuição de "Recusado" para "Em Análise" (ou "Realizado") quando um novo certificado for submetido, solicitando reavaliação.
- Modificar o `CourseDetailsModal.vue` para permitir envio em casos onde já existe um certificado anexado, mas o status não for final (ex. Validado/Concluído).

**Non-Goals:**
- Criar histórico versionado de certificados. Apenas a última versão do certificado importará.
- Permitir alteração de certificados que já estejam "Validados" com sucesso pela UDP/Chefia (a não ser que se decida que isso é válido, mas o padrão será apenas para status pendentes ou recusados).

## Decisions

### 1. Reutilização dos endpoints de upload existentes (Upsert)
- **Decisão:** Modificar os endpoints `POST /api/certificados/upload` e `POST /api/certificados/link` para suportarem lógica de "Upsert" em vez de apenas Insert.
- **Raciocínio:** O frontend já envia o `atribuicao_id`. Se já existir um certificado vinculado a essa atribuição, o backend deve atualizar a entrada existente e deletar o arquivo antigo do disco, em vez de criar um novo registro no banco de dados e deixar o outro órfão, ou retornar erro.

### 2. Controle de Status
- **Decisão:** Quando um certificado for atualizado (re-uploaded), o backend automaticamente alterará o status da atribuição correspondente para `REALIZADO` (que é o status que aguarda validação).
- **Raciocínio:** Se a chefia recusou o certificado (status RECUSADO), enviar um novo certificado é uma submissão para reavaliação.

### 3. Modificação da Interface do Frontend
- **Decisão:** Em `CourseDetailsModal.vue`, o botão para envio de certificado (usando o `emit('send-certificate')` / `<ReuploadCertificateComponent>` ou similar) deve estar visível se o status for `Realizado`, `Em Andamento`, `Recusado`.
- **Raciocínio:** O botão deve estar nomeado "Reenviar Certificado" (ou "Alterar Certificado") quando `hasCertificate` for true e o status permitir.

## Risks / Trade-offs

- **[Risco] Deleção acidental do arquivo em disco:** Ao re-enviar, o arquivo antigo é deletado do diretório `uploads/`. Se o update no banco falhar, o certificado pode ficar quebrado.
  - **Mitigação:** Fazer o update no banco de dados e só deletar o arquivo do disco *após* o commit da transação do BD ser bem sucedido.
- **[Risco] Reenvio de certificado validado:** O usuário pode reenviar acidentalmente (ou maliciosamente) um certificado em uma atribuição já validada.
  - **Mitigação:** Adicionar uma verificação no controller `registrar_certificado_upload` para rejeitar (400 Bad Request) se a atribuição já estiver com status "Validado" ou "Concluído".
