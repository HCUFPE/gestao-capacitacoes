## Why

Nos relatórios de capacitações (Capacitações detalhado, Chefia progresso individual e Consolidado), o usuário precisa navegar manualmente para Gestão de Usuários ou Meus Cursos para ver detalhes de um profissional. Isso quebra o fluxo de trabalho e exige múltiplas navegações para ações simples como verificar o progresso completo de um subordinado ou editar dados de um usuário.

## What Changes

- Adicionar links clicáveis no campo "Nome" / "Profissional" em todas as tabelas de relatório para navegar ao detalhe correspondente
- No relatório de Capacitações (UDP): link leva ao modal de detalhes do usuário com seus cursos e progresso
- No relatório de Chefia: link no nome já existe como botão de modal — manter comportamento e alinhar com padrão
- No relatório Consolidado: link leva ao modal de detalhes do usuário
- Para UDP no relatório de Gestão de Usuários: link direto para edição de perfil do usuário (já existe via botão, adicionar link no nome)
- Respeitar permissões: Chefia acessa apenas subordinados da própria lotação; UDP acessa todos

## Capabilities

### New Capabilities
- `report-user-navigation`: Links clicáveis em tabelas de relatório que abrem detalhes do usuário (cursos, certificados, progresso) respeitando permissões de perfil e lotação

### Modified Capabilities
- `reporting`: Requirement adicional para links de navegação em relatórios (não altera requisitos existentes, adiciona usabilidade)
- `consolidated-report`: Requirement adicional para link no nome do profissional levando ao detalhe do usuário

## Impact

- **Frontend**: `RelatoriosCapacitacoes.vue`, `RelatorioConsolidado.vue`, `RelatoriosChefia.vue` — adicionar links/rotações nos nomes
- **Backend**: Endpoint existente `/api/relatorios/chefia/subordinado/{id}` já serve detalhes; pode ser reutilizado para UDP também via endpoint genérico
- **Rotas**: Possível nova rota `/usuario/{id}` ou reuso do modal de subordinado em outros contextos
- **Permissões**: Backend deve validar que Chefia só acessa subordinados da própria lotação
