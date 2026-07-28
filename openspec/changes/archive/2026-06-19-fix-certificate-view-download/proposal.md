## Why

O sistema falha silenciosamente ao exibir/baixar certificados já enviados pelo usuário na tela Meus Cursos > Detalhe do Curso. Múltiplos bugs impedem o fluxo completo: enum de status inconsistente, dados de certificado não retornados pela API de atribuições, frontend verificando valores de status errados, e endpoint de download com import faltante.

## What Changes

### Backend
- Corrigir `StatusAtribuicao` enum: padronizar valores (`"Realizado"`), adicionar `VALIDADO = "Validado"` e `RECUSADO = "Recusado"`
- Adicionar colunas `data_atribuicao` e `data_validacao` ao modelo `Atribuicao` (referenciados no controller mas inexistentes)
- Incluir `certificado_id`, `certificado_file_path`, `certificado_link` na resposta de `/api/atribuicoes/me`
- Adicionar import faltante `HTTPException` em `main.py` no endpoint de download
- Corrigir validação de certificado para usar os novos valores do enum

### Frontend
- Corrigir `showCertificateButton` em `CourseDetailsModal.vue` para verificar `['REALIZADO', 'CONCLUIDO', 'REALIZADO', 'Validado', 'Concluído']`
- Adicionar tratamento de erro para arquivo inexistente ou link quebrado
- Garantir que certificado enviado por atribuição (não só por inscrição) seja visível

### Specs
- **MODIFIED**: `certificate-validation` — requisitos de download/visualização de certificados

## Capabilities

### New Capabilities

(nenhuma)

### Modified Capabilities

- `certificate-validation`: Adicionar requisitos de visualização/download de certificado já enviado e tratamento de erros

## Impact

- **Backend**: `src/models/atribuicao.py` (enum + colunas), `src/controllers/atribuicao_controller.py` (resposta), `src/main.py` (import), `src/routers/certificado.py` (validação enum)
- **Frontend**: `frontend/src/components/CourseDetailsModal.vue` (status check + error handling)
- **Migration**: Nova migration Alembic para colunas `data_atribuicao` e `data_validacao`
- **API**: `/api/atribuicoes/me` retorna campos adicionais (backward compatible)
- **BREAKING**: Mudança nos valores do enum `StatusAtribuicao` — registros existentes no BD com `"REALIZADO"` podem precisar de data fix
