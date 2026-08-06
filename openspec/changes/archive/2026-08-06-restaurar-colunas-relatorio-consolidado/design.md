## Context

O usuário solicitou que todas as 11 colunas originais sejam exibidas novamente no Relatório Consolidado, em vez de 6, garantindo que o design permaneça elegante através de ícones e badges coloridas.

## Goals / Non-Goals

**Goals:**
- Restaurar o array `headers` com os 11 campos originais.
- Adicionar ícone de check (verde) / x (vermelho) para "Certificado Enviado".
- Manter o link de visualização com ícone para "Certificado".
- Manter a badge colorida para "Status".

**Non-Goals:**
- Alterar APIs do backend ou exportações de Excel/PDF.

## Decisions

- **Estrutura de colunas**:
  ```typescript
  const headers = [
    { text: 'Nome', value: 'nome' },
    { text: 'Vínculo', value: 'vinculo_display' },
    { text: 'Setor', value: 'setor' },
    { text: 'Curso', value: 'nome_curso' },
    { text: 'Plataforma', value: 'certificadora' },
    { text: 'CH', value: 'carga_horaria' },
    { text: 'Ano GD', value: 'ano_gd' },
    { text: 'Status', value: 'status' },
    { text: 'Envio Certificado', value: 'data_envio_certificado' },
    { text: 'Certificado Enviado', value: 'certificado_enviado' },
    { text: 'Certificado', value: 'certificado_link' },
  ];
  ```

## Risks / Trade-offs

- [Risco]: Tabela larga em telas pequenas.
  - *Mitigação*: Uso de container com `overflow-x-auto` no componente `DataTable.vue` para rolagem horizontal suave sem quebrar o layout da página.
