## Why

Atualmente, o Relatório Consolidado exibe os dados consolidados das capacitações dos servidores sem permitir uma filtragem dinâmica por unidade/setor no perfil UDP/Administrativo. A adição desse filtro permite que gestores e a UDP analisem o progresso e adimplência de capacitações por setores específicos.

## What Changes

- **Filtro por Setor/Unidade na Interface**: Adicionar um campo seletor (dropdown) e busca por setor no topo da página do Relatório Consolidado.
- **Filtragem Dinâmica de Dados**: Atualizar a exibição da tabela e métricas consolidadas para reagir ao setor selecionado.
- **Integração na API Backend e Exportações**: Permitir que os endpoints do relatório consolidado e suas exportações (Excel/PDF) aceitem um parâmetro de consulta `setor` / `lotacao` para filtrar os resultados no banco de dados.

## Capabilities

### New Capabilities
- `filtro-setor-relatorio-consolidado`: Suporte a filtro por setor/lotação no Relatório Consolidado (visualização em tela e exportações em Excel/PDF).

### Modified Capabilities

## Impact

- **Frontend**: `frontend/src/views/RelatorioConsolidado.vue` e serviços de relatório.
- **Backend**: `src/routers/relatorio.py` e `src/controllers/relatorio_controller.py`.
- **Testes**: Suíte de testes Pytest no backend e Vitest no frontend.
