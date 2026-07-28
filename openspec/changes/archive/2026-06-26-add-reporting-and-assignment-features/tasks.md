## 1. Granular course assignment (backend)

- [x] 1.1 Criar endpoint POST /api/atribuicoes/lotacao em src/routers/atribuicao.py com body {curso_id, user_ids}
- [x] 1.2 Implementar controller criar_atribuicoes_seletivas em src/controllers/atribuicao_controller.py
- [x] 1.3 Adicionar validação: cada user_id deve pertencer à lotação da chefia (HTTP 403 se não pertencer)
- [x] 1.4 Adicionar validação: chefia sem lotacao retorna HTTP 400
- [x] 1.5 Tratar duplicações (usuario já com curso atribuído) — ignorar ou aviso

## 2. Granular course assignment (frontend)

- [x] 2.1 Adicionar modal/combo de seleção múltipla de usuários na tela de gestão de cursos
- [x] 2.2 Criar endpoint ou reusar existente para listar usuários da lotação da chefia
- [x] 2.3 Exibir apenas usuários sem o curso já atribuído
- [x] 2.4 Adicionar botão "Atribuir a selecionados" e manter "Atribuir a todos"
- [x] 2.5 Conectar frontend ao novo endpoint POST /api/atribuicoes/lotacao

## 3. Vinculo column in reports

- [x] 3.1 Adicionar coluna "Vínculo" ao relatório de progresso individual da chefia (backend — RelatorioProvider.get_progresso_equipe)
- [x] 3.2 Exibir "Não informado" quando vinculo é nulo
- [x] 3.3 Adicionar coluna "Vínculo" na tabela do RelatoriosChefia.vue
- [x] 3.4 Garantir que vinculo já está presente no relatório UDP detalhado (verificar RelatorioProvider.listar_dados_capacitacoes)
- [x] 3.5 Incluir vinculo nas exportações Excel e PDF existentes

## 4. Certificate view in individual progress report

- [x] 4.1 Estender get_progresso_equipe para incluir certificado_id, certificado_file_path, certificado_link do último certificado por curso
- [x] 4.2 Adicionar coluna/link "Visualizar certificado" no RelatoriosChefia.vue (via modal de detalhes do subordinado)
- [x] 4.3 Abrir certificado mais recente ao clicar no link

## 5. User detail link from progress report

- [x] 5.1 Criar view/modal de detalhes do subordinado (cursos, status, certificados)
- [x] 5.2 Adicionar roteamento Vue para a nova view
- [x] 5.3 Tornar nome do usuário clicável no relatório de progresso
- [x] 5.4 Criar endpoint backend para dados do subordinado (ou reusar endpoints existentes)
- [x] 5.5 Validar permissão: chefia só acessa subordinados da própria lotação

## 6. Report filters (year and vinculo)

- [x] 6.1 Adicionar query params ?ano= e ?vinculo= ao endpoint GET /api/relatorios/chefia/status-lotacao
- [x] 6.2 Adicionar query params ?ano= e ?vinculo= ao endpoint GET /api/relatorios/chefia/progresso-individual
- [x] 6.3 Adicionar query params ?ano= e ?vinculo= ao endpoint GET /api/relatorios/capacitacoes (UDP)
- [x] 6.4 Aplicar filtros nas queries SQL do RelatorioProvider (usar data_conclusao para ano)
- [x] 6.5 Adicionar componentes de filtro (dropdowns) no RelatoriosChefia.vue
- [x] 6.6 Adicionar componentes de filtro (dropdowns) no RelatoriosCapacitacoes.vue
- [x] 6.7 Filtros aplicados às exportações (passar params para os controllers de export)

## 7. Consolidated report for Mentor

- [x] 7.1 Criar endpoint GET /api/relatorios/chefia/consolidado no router de relatórios
- [x] 7.2 Implementar controller que retorna: nome, curso, status, data_envio_certificado, vinculo, certificado_enviado
- [x] 7.3 Criar endpoint GET /api/relatorios/udp/consolidado (mesma lógica, sem filtro de lotação)
- [x] 7.4 Criar exportação Excel para relatório consolidado (chefia e UDP)
- [x] 7.5 Criar exportação PDF para relatório consolidado (chefia e UDP)
- [x] 7.6 Criar view/frontend para relatório consolidado com botão de visualizar certificado
- [x] 7.7 Aplicar filtros de ano e vínculo ao relatório consolidado

## 8. Testing and validation

- [x] 8.1 Testar atribuição granular: chefia seleciona 3 usuários → 3 atribuições criadas
- [x] 8.2 Testar permissão: chefia tenta atribuir usuário de outro setor → HTTP 403
- [x] 8.3 Testar filtros: ano + vínculo combinados retornam dados corretos
- [x] 8.4 Testar vinculo "Não informado" para usuário sem vinculo
- [x] 8.5 Testar visualização de certificado no progresso individual
- [x] 8.6 Testar link para detalhes do subordinado
- [x] 8.7 Testar relatório consolidado: dados completos, exportações funcionais
- [x] 8.8 Validar que todas as exportações incluem vinculo e respeitam filtros
