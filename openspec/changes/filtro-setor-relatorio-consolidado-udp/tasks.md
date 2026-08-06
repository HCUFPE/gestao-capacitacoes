## 1. Backend Implementation

- [x] 1.1 Atualizar o router `src/routers/relatorio.py` para aceitar o parâmetro de consulta `lotacao` opcional no endpoint `/api/relatorios/udp/consolidado`.
- [x] 1.2 Atualizar os endpoints de exportação em Excel e PDF (`/udp/consolidado/export/excel` e `/pdf`) para aceitar o parâmetro `lotacao` e filtrar os dados.
- [x] 1.3 Escrever testes automatizados Pytest em `tests/` validando a filtragem por setor nas rotas do relatório consolidado e exportações.

## 2. Frontend Implementation

- [x] 2.1 Adicionar seletor de setor (dropdown) no topo da visualização do `RelatorioConsolidado.vue`.
- [x] 2.2 Implementar a reatividade na tabela e cards do `RelatorioConsolidado.vue` para aplicar o filtro por setor selecionado.
- [x] 2.3 Atualizar os handlers de download de Excel e PDF no frontend para passar a `lotacao` selecionada na URL da requisição.
- [x] 2.4 Escrever testes automatizados Vitest em `frontend/src/views/RelatorioConsolidado.test.ts` cobrindo a filtragem por setor e emissão de eventos.
