## Context

Atualmente, os relatórios de capacitações exibir dados tabulares (nome, curso, status, etc.) sem links de navegação para detalhes do usuário. A única exceção é o relatório da Chefia (`RelatoriosChefia.vue`), onde o nome do subordinado já abre um modal com detalhes via chamada a `/api/relatorios/chefia/subordinado/{id}`. Os outros relatórios (Capacitações detalhado e Consolidado) não possuem essa funcionalidade, exigindo que o usuário navegue manualmente.

O endpoint `/api/relatorios/chefia/subordinado/{id}` já retorna os cursos, status e certificados de um usuário — pode ser estendido para uso da UDP também.

## Goals / Non-Goals

**Goals:**
- Permitir clique no nome do profissional em todos os relatórios para abrir detalhes
- Reutilizar o padrão de modal já existente no relatório da Chefia
- Respeitar permissões: Chefia acessa apenas sua lotação, UDP acessa todos
- Manter consistência visual e de UX entre os relatórios

**Non-Goals:**
- Não criar uma página de detalhe dedicada (SPA route) — usar modal
- Não alterar a estrutura de dados do backend significativamente
- Não adicionar links no relatório UDP dashboard (RelatoriosUdp.vue) — focar nas tabelas com dados de profissionais

## Decisions

### Decisão 1: Reutilizar modal existente vs. criar componente compartilhado

**Escolha**: Criar um componente reutilizável `UserDetailsModal.vue` extraído do modal de subordinado da Chefia.

**Rationale**: O modal atual em `RelatoriosChefia.vue` é inline no componente. Extrair para um componente reutilizável permite uso em `RelatoriosCapacitacoes.vue` e `RelatorioConsolidado.vue` sem duplicação. O componente recebe `userId`, carrega dados via API e exibe cursos/certificados.

**Alternativas consideradas**:
- Duplicar o modal em cada view — mais código, mais manutenção
- Criar rota dedicada `/usuario/{id}` — mais complexo, muda o fluxo de navegação

### Decisão 2: Endpoint unificado para detalhes do usuário

**Escolha**: Criar endpoint genérico `GET /api/relatorios/usuario/{user_id}/detalhes` que reutiliza a lógica de `/api/relatorios/chefia/subordinado/{id}` mas aplica permissões baseadas no perfil do request.

**Rationale**: Evita duplicação de lógica. A validação de permissão (Chefia só acessa sua lotação) é feita no controller.

**Alternativas consideradas**:
- Usar o endpoint da chefia diretamente — acopla views da UDP a rotas de chefia
- Criar endpoint separado para UDP — duplicação desnecessária

### Decisão 3: Link vs. botão para navegação

**Escolha**: Manter o padrão de link clicável no nome (texto azul com hover) conforme já feito na Chefia, para consistência visual.

## Risks / Trade-offs

[Modal pode ficar grande com muitos cursos] → Mitigação: usar DataTable com paginação dentro do modal, similar ao relatório consolidado

[Chefia sem lotação não deve acessar detalhes de qualquer usuário] → Mitigação: validação backend no controller verificando lotação do request user

[Performance com muitas chamadas API se usuário clicar rapidamente] → Mitigação: debounce no clique e loading state no modal
