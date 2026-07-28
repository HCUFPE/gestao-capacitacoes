## 1. Backend — Endpoint de Download

- [x] 1.1 Em `src/main.py`, usar `mimetypes.guess_type()` para resolver o Content-Type correto baseado na extensão do arquivo no endpoint `download_certificado`.
- [x] 1.2 Alterar o cabeçalho `Content-Disposition` de `attachment` para `inline` no `FileResponse`.

## 2. Frontend — Função Utilitária Compartilhada

- [x] 2.1 Criar `frontend/src/services/certificateUtils.ts` com a função `getCertificateUrl(item)` que usa sempre a rota `/api/certificados/download/` e trata `certificado_link` como fallback externo.
- [x] 2.2 Substituir `getCertificateUrl` inline em `RelatoriosChefia.vue` pela função utilitária importada.
- [x] 2.3 Substituir `getCertificateUrl` inline em `RelatorioConsolidado.vue` pela função utilitária importada.
- [x] 2.4 Substituir `getCertificateUrl` inline em `UserDetailsModal.vue` pela função utilitária importada.

## 3. Frontend — CourseDetailsModal

- [x] 3.1 Remover a requisição `fetch HEAD` em `handleCertificateButtonClick` do `CourseDetailsModal.vue`, substituindo por `window.open` direto.
- [x] 3.2 Alterar o `certificateButtonText` para retornar "Visualizar Certificado" em vez de "Baixar Certificado" para arquivos PDF.
- [x] 3.3 Atualizar `certificateUrl` no `CourseDetailsModal.vue` para usar a função utilitária compartilhada.

## 4. Testes Automatizados

- [x] 4.1 Escrever teste `pytest` para o endpoint `download_certificado` validando Content-Type correto para `.pdf`, `.png`, `.jpg` e Content-Disposition `inline`.
- [x] 4.2 Escrever teste `vitest` para `certificateUtils.ts` validando a construção correta de URLs para `certificado_file_path` e `certificado_link`.
- [x] 4.3 Executar `pytest` e `npx vitest run` para verificar que todos os testes passam.
