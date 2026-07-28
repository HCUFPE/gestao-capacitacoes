## Context

O sistema de gestão de capacitações possui funcionalidades básicas de relatórios e atribuição, porém carece de recursos importantes para uso produtivo pela chefia e pela UDP:

1. **Atribuição de cursos**: Atualmente, `criar_atribuicoes_para_lotacao` atribui o curso a TODOS os usuários de uma lotação. Não há como selecionar indivíduos.
2. **Relatórios da chefia**: O progresso individual não mostra certificados, vínculo, nem permite clicar no usuário para ver detalhes.
3. **Relatórios UDP**: Não incluem filtros por ano ou vínculo, e não há relatório consolidado específico para comprovação no Mentor.
4. **Vínculo**: O campo `vinculo` já existe no modelo Usuario e já é incluído no relatório detalhado da UDP (`listar_dados_capacitacoes`), porém não aparece nos relatórios de chefia nem como filtro.
5. **Data de submissão**: O modelo Atribuicao já possui `data_conclusao` (setada quando certificado é enviado), que pode ser usada para filtro por ano.

## Goals / Non-Goals

**Goals:**
- Atribuição granular: chefia seleciona curso + pessoas específicas da equipe
- Vínculo visível em todos os relatórios e exportações
- Filtros por ano (data de envio do certificado) e por vínculo
- Visualização de certificado no relatório de progresso individual
- Link para detalhes do usuário a partir do relatório
- Relatório consolidado para comprovação no Mentor

**Non-Goals:**
- Nova tela de validação de certificados (item 11)
- Correções de falhas de certificado/PDF (change `fix-certificates-and-pdf`)

## Decisions

**Decision 1: Novo endpoint para atribuição granular**
- Criar `POST /api/atribuicoes/lotacao` com body `{curso_id, user_ids: []}`.
- Validação backend: cada user_id deve pertencer à mesma lotação da chefia.
- Alternativa considerada: modificar endpoint existente — rejeitada para não quebrar comportamento atual de atribuição em massa.

**Decision 2: Filtros via query params nos endpoints existentes**
- Adicionar `?ano=YYYY&vinculo=X` aos endpoints de relatórios da chefia e UDP.
- Filtros aplicados na query SQL via `.where()`, não no frontend.
- Exportações respeitam os mesmos filtros.

**Decision 3: Relatório consolidado como novo endpoint**
- Criar `GET /api/relatorios/chefia/consolidado` (e equivalente para UDP se necessário).
- Retorna dados tabulares: nome, curso, status, data_envio, vinculo, tem_certificado.
- Exportação PDF e Excel incluídas.
- Alternativa considerada: reusar relatório existente com flag — rejeitada porque o consolidado tem formato e campos diferentes.

**Decision 4: Certificado no progresso individual via dados existentes**
- O `get_progresso_equipe` do RelatorioProvider já faz join com Atribuicao. Estender para incluir certificado_id, certificado_file_path, certificado_link, data_conclusao do último certificado por curso.
- Frontend exibe ícone/link "Visualizar certificado" quando certificado existe.

**Decision 5: Link para detalhes do usuário via frontend routing**
- Não há tela dedicada de "detalhes do usuário" no frontend atualmente. Criar uma seção/modal que mostra cursos, certificados e progresso do subordinado.
- Alternativa: reusar CourseDetailsModal — não se aplica, pois é para cursos, não para usuários.

**Decision 6: Seleção de usuários na UI de atribuição**
- Adicionar modal/combo de múltipla seleção na tela de gestão de cursos (GestaoCursos.vue) ou criar componente dedicado.
- Listar apenas usuários da lotação da chefia que ainda não têm o curso atribuído.

## Risks / Trade-offs

[Performance de consultas com múltiplos filtros] → Queries com JOINs em Usuario, Atribuicao, Curso, Certificado podem ficar lentas. Mitigation: índices em lotacao, vinculo, data_conclusao.

[Atribuição granular vs em massa] → Manter ambos os fluxos. UI deve deixar claro qual está sendo usado. Mitigation: botão separado "Atribuir a selecionados" vs "Atribuir a todos".

[Detalhes do usuário — nova tela] → Adicionar roteamento Vue para nova view. Mitigation: criar view simples focada em cursos/certificados do subordinado.
