## Context

O fluxo de visualização/download de certificado está quebrado por 5 bugs interligados:

1. **Enum inconsistente**: `REALIZADO = "REALIZADO"` (maiúsculas) vs outros valores com Title Case. Faltam `VALIDADO` e `RECUSADO` → `validar_certificado` crashes com `AttributeError`.
2. **Frontend verifica valores errados**: `showCertificateButton` check `['REALIZADO', 'VALIDADO']` mas backend retorna `"Concluído"` para validados.
3. **API de atribuições não retorna dados do certificado**: `listar_atribuicoes_por_usuario` eager-loads `certificado` relationship mas só retorna `{id, status, atribuido_em, curso}` — falta `certificado_id`, `file_path`, `link`.
4. **`HTTPException` não importado**: `main.py` usa `HTTPException` no download endpoint sem import.
5. **Colunas inexistentes**: Controller referencia `data_atribuicao` e `data_validacao` que não existem no modelo.

## Goals / Non-Goals

**Goals:**
- Corrigir enum `StatusAtribuicao` e migrar dados existentes
- Incluir dados de certificado nas respostas de `/api/atribuicoes/me` e `/api/inscricoes/me`
- Adicionar colunas faltantes ao modelo `Atribuicao`
- Corrigir `showCertificateButton` no frontend para todos os status válidos
- Adicionar tratamento de erro para download (arquivo inexistente, link quebrado, permissão)

**Non-Goals:**
- Refatorar toda a arquitetura de certificados
- Adicionar validação automática de certificados (OCR, etc.)
- Mudar formato de armazenamento (continua sendo file_path ou link)

## Decisions

### 1. Normalizar enum para Title Case com data fix

Mudar `"REALIZADO"` → `"Realizado"`. Adicionar `"Validado"` e `"Recusado"`. Criar migration Alembic com op.execute para converter registros existentes.

**Alternativa considerada**: Manter `"REALIZADO"` e ajustar o frontend — rejeitada porque quebra a consistência do enum e não resolve a falta de VALIDADO/RECUSADO.

### 2. Adicionar certificado data via controller, não schema

O controller `listar_atribuicoes_por_usuario` já retorna dict manual. Vou adicionar os campos de certificado diretamente — não precisa mudar o Pydantic schema da API de atribuições pois `response_model` já aceita campos extras com `Config.from_attributes`.

**Alternativa considerada**: Criar novo schema Pydantic — rejeitada pois o controller retorna dicts manuais, não models.

### 3. Frontend verificar status case-insensitive

Normalizar para `.toUpperCase()` no frontend para evitar mismatch entre Title Case e maiúsculas.

**Alternativa considerada**: Ajustar backend para retornar sempre maiúsculas — rejeitada pois Title Case é padrão nos demais valores do enum.

## Risks / Trade-offs

| Risco | Mitigação |
|---|---|
| Data fix do enum quebra atribuições em andamento | Migration com WHERE clause específica, rollback via migration reversa |
| Frontend cache com status antigo | Clear cache ou version bump do build |
| Arquivos físicos existindo sem registro no BD (ou vice-versa) | Tratamento de erro 404 no download endpoint |
