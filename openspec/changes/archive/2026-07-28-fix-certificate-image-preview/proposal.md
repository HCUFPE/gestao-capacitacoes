## Why

Usuários e gestores não conseguem visualizar imagens de certificados enviados (PNG, JPG, etc.) diretamente no navegador após o envio. O backend força download automático com `Content-Disposition: attachment` e usa `application/octet-stream` para imagens. Além disso, existem 3 componentes (`RelatoriosChefia.vue`, `RelatorioConsolidado.vue`, `UserDetailsModal.vue`) que montam URLs de certificado como `/static/uploads/...`, mas esse caminho **não é servido pelo FastAPI** — só `/assets` está montado. Essas URLs caem no catch-all do Vue Router e nunca funcionam.

## What Changes

- Corrigir o endpoint de download no backend para servir arquivos com o `Content-Type` correto e cabeçalho `Content-Disposition: inline`.
- Remover a requisição `fetch HEAD` no frontend que causa problemas de CORS.
- **Unificar a construção de URL de certificado** em uma função utilitária compartilhada, substituindo o padrão quebrado `/static/uploads/` pela rota da API `/api/certificados/download/` em todos os componentes.
- Ajustar o texto do botão de certificado no `CourseDetailsModal` para refletir o comportamento de visualização inline.

## Capabilities

### New Capabilities
- `certificate-preview`: Visualização inline e direta de arquivos de certificado (PDF e imagens) no navegador, com URL unificada via rota da API.

### Modified Capabilities
<!-- Nenhuma capability existente tem seus requisitos de spec alterados. -->

## Impact

- **Backend:** `src/main.py` — endpoint `/api/certificados/download/{file_name}`
- **Frontend — afetados diretamente:**
  - `CourseDetailsModal.vue` — remoção do HEAD fetch, ajuste texto do botão
  - `ValidacaoCertificados.vue` — sem HEAD fetch (já ok), mas usa rota da API
  - `RelatoriosChefia.vue` — URL quebrada `/static/uploads/` → rota da API
  - `RelatorioConsolidado.vue` — URL quebrada `/static/uploads/` → rota da API
  - `UserDetailsModal.vue` — URL quebrada `/static/uploads/` → rota da API
- **Novo arquivo:** função utilitária compartilhada para construção de URL de certificado
