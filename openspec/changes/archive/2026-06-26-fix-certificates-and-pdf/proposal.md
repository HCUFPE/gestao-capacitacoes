## Why

Três falhas operacionais impactam diretamente a experiência do usuário: (1) certificados já enviados não podem ser visualizados/baixados adequadamente em Meus Cursos; (2) o usuário não consegue substituir um certificado enviado incorretamente sem se desinscrever do curso; (3) a exportação PDF corta conteúdo (nomes, cursos, vínculo, datas, status). Essas falhas impedem o fluxo normal de comprovação de capacitações.

## What Changes

- **Visualização/download de certificado**: Garantir que o botão de visualização/baixa de certificado funcione em Meus Cursos e no modal de detalhes, com tratamento de erro para arquivos inexistentes.
- **Substituição de certificado**: Adicionar botão "Reenviar certificado" que permite upload de novo certificado sem perder a inscrição, mantendo apenas o certificado mais recente como ativo.
- **Exportação PDF sem cortes**: Revisar layout, margens, larguras de coluna, quebras de linha e paginação no helper de PDF para garantir que nenhum campo seja cortado.

## Capabilities

### New Capabilities
- `certificate-replacement`: User can re-upload/replace a certificate without withdrawing from the course. Only the latest certificate per user+course is considered active.

### Modified Capabilities
- `certificate-validation`: Adding requirements for re-upload flow, error handling improvements, and ensuring the download/view endpoints work correctly in all contexts (Meus Cursos, CourseDetailsModal).
- `reporting`: Adding requirements for PDF export layout fixes (no content truncation), proper column widths, margins, and page breaks.

## Impact

- **Backend**: `src/routers/certificado.py` (nova rota de re-upload), `src/controllers/certificado_controller.py` (lógica de substituição), `src/controllers/atribuicao_controller.py` (preservação de inscrição), `src/helpers/pdf_helper.py` (layout correto), `src/models/certificado.py` (possível campo para marcar certificado ativo).
- **Frontend**: `frontend/src/components/CourseDetailsModal.vue` (botão reenviar), `frontend/src/components/CertificateUploadModal.vue` (suporte a reenvio), `frontend/src/views/MeusCursos.vue` (botão de reenvio nos cards), `frontend/src/views/RelatoriosCapacitacoes.vue` (se necessário).
- **API**: Novo endpoint POST ou reuso do existente para substituição de certificado.
