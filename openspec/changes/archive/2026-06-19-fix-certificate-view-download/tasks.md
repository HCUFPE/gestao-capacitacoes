## 1. Fix StatusAtribuicao enum (src/models/atribuicao.py)

- [x] 1.1 Normalizar `REALIZADO = "REALIZADO"` para `REALIZADO = "Realizado"`
- [x] 1.2 Adicionar `VALIDADO = "Validado"` e `RECUSADO = "Recusado"` ao enum
- [x] 1.3 Adicionar colunas `data_atribuicao` (DateTime) e `data_validacao` (DateTime) ao modelo Atribuicao

## 2. Create Alembic migration

- [x] 2.1 Gerar migration para adicionar colunas `data_atribuicao` e `data_validacao`
- [x] 2.2 Adicionar data fix na migration: `UPDATE atribuicoes SET status='Realizado' WHERE status='REALIZADO'`

## 3. Fix certificate download endpoint (src/main.py)

- [x] 3.1 Adicionar import `from fastapi import HTTPException`
- [x] 3.2 Garantir que o endpoint `/api/certificados/download/{file_name}` funciona corretamente

## 4. Include certificate data in assignment response (src/controllers/atribuicao_controller.py)

- [x] 4.1 Adicionar `certificado_id`, `certificado_file_path`, `certificado_link` à resposta de `listar_atribuicoes_por_usuario`

## 5. Fix certificate validation endpoint (src/routers/certificado.py)

- [x] 5.1 Atualizar validação de status para usar `StatusAtribuicao.VALIDADO` e `StatusAtribuicao.RECUSADO`

## 6. Fix frontend certificate display (frontend/src/components/CourseDetailsModal.vue)

- [x] 6.1 Corrigir `showCertificateButton` para verificar status normalizados (`['Realizado', 'REALIZADO', 'Concluído', 'Validado']`)
- [x] 6.2 Adicionar tratamento de erro (try/catch ou error handler) para download de certificado
- [x] 6.3 Adicionar mensagem de erro amigável para arquivo inexistente ou link quebrado
