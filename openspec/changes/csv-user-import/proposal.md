## Why

Atualmente, a importação de usuários via CSV só pode ser executada manualmente via linha de comando rodando o script `import_users.py`. Isso impede que administradores do sistema realizem a carga de novos usuários ou a atualização de cadastros de forma autônoma e segura diretamente pela interface web.

## What Changes

- **Novo Endpoint Backend**: Criar um endpoint na API (`POST /admin/usuarios/importar-csv`) protegido para o perfil de administrador (UDP / Admin), que aceita o envio de arquivo CSV via `multipart/form-data`, valida o formato e executa a importação/sincronização de usuários no banco de dados.
- **Nova Interface Frontend**: Criar um componente modal/tela no painel administrativo do frontend (Vue 3) permitindo upload de arquivo CSV, exibição de pré-visualização/feedback do progresso e resumo dos resultados (quantidade de usuários inseridos, atualizados e erros).

## Capabilities

### New Capabilities
- `csv-user-import`: Permite o envio de arquivos CSV via interface web para cadastro e atualização em lote de usuários com validações e feedback estruturado.

### Modified Capabilities
<!-- Nenhuma funcionalidade pré-existente tem seus requisitos alterados -->

## Impact

- **Backend**: Adição de endpoint no `src/routers/admin.py` (ou `usuario.py`), reutilização/refatoração da lógica de parsing e inserção em `src/controllers/usuario_controller.py` ou utilitário desacoplado de `import_users.py`.
- **Frontend**: Adição de serviço em `src/services/adminService.ts` / `usuarioService.ts` e componente/modal de importação na view de administração (`AdminView.vue` / `UsuariosView.vue`).
- **Segurança & Permissões**: Apenas usuários autenticados com permissão de administrador (`is_udp`) terão acesso ao endpoint e ao botão na interface.
