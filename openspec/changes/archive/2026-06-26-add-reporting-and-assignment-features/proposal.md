## Why

O sistema carece de funcionalidades essenciais para a gestão eficiente de capacitações: atribuição granular de cursos por chefia, visualização de certificados nos relatórios, filtros por ano e vínculo, e um relatório consolidado para comprovação no sistema Mentor. Sem essas funcionalidades, a chefia e a UDP gastam tempo excessivo em tarefas manuais e não conseguem comprovar conformidade de forma eficiente.

## What Changes

- **Atribuição granular de cursos**: Chefia pode selecionar um curso e escolher pessoas específicas da equipe (em vez de atribuir para toda a lotação).
- **Visualização de certificado nos relatórios**: Botão/link "Visualizar certificado" nas linhas do relatório de progresso individual da chefia.
- **Link para detalhe do usuário/progresso a partir do relatório**: Clique no nome do usuário leva ao detalhe de progresso.
- **Coluna "Vínculo" nos relatórios**: Incluir vínculo do usuário nos relatórios da chefia e UDP, incluindo exportações.
- **Filtro por ano**: Filtrar relatórios pela data de envio do certificado.
- **Filtro por vínculo**: Filtrar relatórios por vínculo específico ou "Todos".
- **Relatório consolidado para Mentor**: Relatório com nome, curso, status, data de envio, vínculo e indicação de certificado, para comprovação sem baixar certificado individualmente.

## Capabilities

### New Capabilities
- `granular-course-assignment`: Chefia can select specific team members for course assignment instead of assigning to entire lotacao.
- `report-filters`: Filter reports by year (certificate submission date) and by vinculo (employment type).
- `consolidated-report`: Consolidated report for Mentor compliance proof with all relevant fields in a single view/export.

### Modified Capabilities
- `reporting`: Adding certificate view links, user detail links, vinculo column, filters, and consolidated report to existing reporting specs.
- `course-assignment`: Adding granular assignment capability (select specific users) to existing assignment specs.

## Impact

- **Backend**: `src/routers/atribuicao.py` (nova rota de atribuição granular), `src/controllers/atribuicao_controller.py` (lógica de atribuição seletiva), `src/controllers/relatorio_controller.py` (filtros e campos adicionais), `src/providers/implementations/relatorio_provider.py` (query com vinculo, filtros, data_submissao), `src/routers/relatorio.py` (query params de filtro).
- **Frontend**: `frontend/src/views/RelatoriosChefia.vue` (botões de certificado, links de usuário, filtros), `frontend/src/views/RelatoriosCapacitacoes.vue` (filtros, botão de certificado), `frontend/src/views/GestaoCursos.vue` (seleção granular de usuários), novo componente de filtros.
- **API**: Novo endpoint POST para atribuição granular, query params `?ano=&vinculo=` nos endpoints de relatório, novo endpoint para relatório consolidado.
