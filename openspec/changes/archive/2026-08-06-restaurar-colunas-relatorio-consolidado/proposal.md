## Why

A simplificação anterior reduziu a quantidade de colunas do Relatório Consolidado para 6. O usuário solicitou que todas as 11 colunas originais sejam mantidas e exibidas na tabela da tela, mas combinando o uso de iconografia (ícones informativos/visuais) e *color coding* (destaque de cores) para manter a tabela limpa e responsiva.

## What Changes

- Restaurar as 11 colunas originais na tabela do `RelatorioConsolidado.vue`:
  1. **Nome**
  2. **Vínculo**
  3. **Setor**
  4. **Curso**
  5. **Plataforma**
  6. **CH**
  7. **Ano GD**
  8. **Status** (com *color coding* em badge)
  9. **Envio Certificado** (data de envio)
  10. **Certificado Enviado** (com ícone verde de check ou vermelho de X)
  11. **Certificado** (botão/link com ícone de documento para visualização do arquivo)
- Adicionar rolagem horizontal suave (`overflow-x-auto`) e ajuste visual inteligente das colunas para suportar as 11 colunas sem deformar o layout.

## Capabilities

### New Capabilities
- `full-consolidated-report-layout`: Layout de 11 colunas no Relatório Consolidado com suporte a ícones e badges coloridos.

### Modified Capabilities

## Impact

- Frontend: `frontend/src/views/RelatorioConsolidado.vue`
- Testes: Teste no Vitest para validar a renderização das 11 colunas.
