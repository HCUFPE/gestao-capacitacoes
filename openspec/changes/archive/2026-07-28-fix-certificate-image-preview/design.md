## Context

O backend expõe a rota `/api/certificados/download/{file_name}` em `src/main.py`. Ao acessar essa URL, a resposta retorna cabeçalhos de download forçado (`Content-Disposition: attachment`) e define o `media_type` como `"application/octet-stream"` para imagens. O frontend tenta validar a existência do arquivo fazendo um pré-fetch `HEAD` antes de abrir a aba, o que gera erros de CORS.

Além do problema de MIME/headers, existem **3 componentes** que constroem URLs de certificado como `/static/uploads/${fileName}` — mas essa rota estática **nunca foi montada** no FastAPI. Apenas `/assets` está montado (apontando para `src/static/dist/assets`). Essas URLs caem no catch-all `/{full_path:path}` que retorna o `index.html` do Vue, não o arquivo. Esses links estão silenciosamente quebrados.

Os 3 componentes afetados:
- `RelatoriosChefia.vue` → `getCertificateUrl()`
- `RelatorioConsolidado.vue` → `getCertificateUrl()`
- `UserDetailsModal.vue` → `getCertificateUrl()`

Enquanto `CourseDetailsModal.vue` e `ValidacaoCertificados.vue` já usam a rota da API correta.

## Goals / Non-Goals

**Goals:**
- Permitir a visualização inline de certificados (imagens e PDFs) no navegador.
- Unificar a construção de URL de certificado em uma função utilitária compartilhada.
- Corrigir os links de certificado que estão silenciosamente quebrados nos relatórios.
- Evitar erros de CORS ao visualizar certificados.
- Manter coerência entre texto do botão e comportamento real.

**Non-Goals:**
- Adicionar autenticação à rota de download de certificados (possível melhoria futura, fora de escopo).
- Alterar o local de armazenamento dos arquivos de certificado.
- Alterar o banco de dados.

## Decisions

### 1. Mapeamento de Tipos MIME no Backend
- **Decisão:** Usar `mimetypes.guess_type()` do Python stdlib na rota `/api/certificados/download/{file_name}` de `src/main.py` para resolver o tipo MIME correto baseado na extensão do arquivo, com fallback para `application/octet-stream`.
- **Alternativa Considerada:** Mapeamento manual explícito (`dict` de extensão → MIME). Descartado por ser menos extensível e redundante com a stdlib.

### 2. Cabeçalho de Disposição Inline
- **Decisão:** Substituir `attachment` por `inline` no cabeçalho `Content-Disposition` do `FileResponse`.
- **Raciocínio:** O valor `inline` instrui o navegador a tentar exibir o arquivo diretamente quando o formato é suportado (PDF, imagens comuns).

### 3. Remoção do Pré-fetch HEAD no Frontend
- **Decisão:** Em `CourseDetailsModal.vue`, remover a requisição `fetch(..., { method: 'HEAD' })` e fazer `window.open(url, '_blank')` diretamente.
- **Raciocínio:** Se o arquivo não existir, a própria API responde com 404. O fetch HEAD cross-origin aciona validações de CORS desnecessárias.

### 4. Função Utilitária Compartilhada para URL de Certificado
- **Decisão:** Criar um arquivo `frontend/src/services/certificateUtils.ts` com uma função `getCertificateUrl(item)` que usa sempre a rota `/api/certificados/download/`. Substituir as implementações inline duplicadas nos 5 componentes.
- **Alternativa Considerada:** Corrigir cada `getCertificateUrl` individualmente. Descartado porque manteria a duplicação e o risco de divergência futura.

### 5. Texto do Botão Coerente
- **Decisão:** Alterar o texto do botão em `CourseDetailsModal.vue` de "Baixar Certificado" para "Visualizar Certificado" para PDFs, refletindo o comportamento inline.

## Risks / Trade-offs

- **[Risco]** Navegadores muito antigos podem não renderizar certos tipos de imagem inline e forçar download.
  - **Mitigação:** Comportamento padrão e seguro do navegador; não afeta a usabilidade da maioria dos usuários.
- **[Risco]** A rota de download não exige autenticação — qualquer pessoa com a URL pode acessar o certificado.
  - **Mitigação:** Os nomes de arquivo são UUIDs, provendo obscuridade. Adicionar autenticação é uma melhoria futura fora deste escopo.
