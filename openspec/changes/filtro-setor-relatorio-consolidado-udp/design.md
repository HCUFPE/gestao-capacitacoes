## Context

O Relatório Consolidado exibe dados agregados sobre capacitações e servidores. Na visualização de chefia, os dados são escopados pela própria lotação. No entanto, no modo UDP / Administrador (`/relatorios/consolidado/udp`), é necessário permitir a filtragem por qualquer setor (lotação) cadastrado no sistema.

## Goals / Non-Goals

**Goals:**
- Adicionar um seletor de setor/lotação no topo do `RelatorioConsolidado.vue`.
- Atualizar a reatividade da tabela e das estatísticas para refletir o setor selecionado no frontend.
- Atualizar os endpoints de exportação (`/api/relatorios/udp/consolidado/export/excel` e `/pdf`) e a busca consolidada no backend para aceitar o parâmetro `lotacao` / `setor`.

**Non-Goals:**
- Alterar o esquema de tabelas ou criar novas entidades no banco de dados.

## Decisions

- **Decisão 1: Extração Dinâmica da Lista de Lotações**:
  - Extrair dinamicamente a lista de lotações únicas a partir dos registros do relatório consolidado ou reutilizar endpoint de lotações para preencher o dropdown de filtro.
- **Decisão 2: Filtragem Reativa no Frontend e Parâmetro nas Exportações**:
  - Filtragem em tempo real na tabela Vue via propriedade `computed`.
  - Envio do parâmetro `lotacao` via query query params nas requisições de download de Excel e PDF para manter o arquivo exportado consistente com a visão da tela.

## Risks / Trade-offs

- [Registros com Lotação Nula/Vazia] → Tratar registros sem lotação com o rótulo "Sem Lotação Definida" para que também possam ser filtrados.
