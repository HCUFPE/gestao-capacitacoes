## Why

Quando um usuário faz o upload de um arquivo incorreto como certificado, ele atualmente não tem como alterar o arquivo enviado sem se desinscrever do curso inteiro. Isso gera atrito, perda de histórico e frustração, exigindo que o usuário recomece o fluxo de inscrição e registro de conclusão do zero.

## What Changes

- Adicionar suporte na API (backend) para atualização/sobrescrita de um arquivo de certificado existente vinculado a uma atribuição/inscrição do usuário.
- Adicionar um botão de "Reenviar Certificado" ou funcionalidade similar na interface de detalhes do curso (`CourseDetailsModal.vue`) para certificados enviados erroneamente ou rejeitados pela validação (que precisem de correção).
- Atualizar a interface para refletir o novo status imediatamente.
- Garantir que o envio de um novo certificado limpe um eventual status de "Recusado" ou "Rejeitado" se a validação falhou anteriormente.

## Capabilities

### New Capabilities
- `certificate-reupload`: Fluxo completo para substituição de arquivo de certificado em uma atribuição existente sem desinscrição.

### Modified Capabilities
<!-- Nenhuma requirement de funcionalidade existente será alterada no nível da spec. -->

## Impact

- **Backend:** `src/main.py` e/ou `src/routers/certificado.py` para endpoints de upload/update. Atualização do `DatabaseManager` ou models associados para apontar para o novo arquivo/link.
- **Frontend:** `CourseDetailsModal.vue` e serviços de API relacionados ao envio de certificado.
- **Armazenamento:** Limpeza de arquivos antigos órfãos no diretório `/static/uploads/` após o reenvio bem-sucedido (se aplicável).
