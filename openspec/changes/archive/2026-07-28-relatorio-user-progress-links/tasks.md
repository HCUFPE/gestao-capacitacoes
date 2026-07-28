## 1. Backend - Endpoint unificado para detalhes do usuário

- [x] 1.1 Criar função `get_usuario_detalhes` no `src/controllers/relatorio_controller.py` que consulta as atribuições de um usuário com cursos e certificados (reutilizar lógica de `get_subordinado_detalhes` do router)
- [x] 1.2 Criar função de validação de permissão no controller: Chefia só acessa usuários da mesma lotação; UDP acessa qualquer usuário
- [x] 1.3 Adicionar endpoint `GET /api/relatorios/usuario/{user_id}/detalhes` no `src/routers/relatorio.py` com dependência de auth que aceita Chefia e UDP
- [x] 1.4 Adicionar função de helper `can_access_user_details(current_user, target_user_id, db)` para centralizar a vermissão de permissão

## 2. Backend - Tests

- [x] 2.1 Escrever pytest em `tests/test_usuario_detalhes_endpoint.py`: teste happy path - UDP acessa detalhes de qualquer usuário
- [x] 2.2 Escrever pytest: teste happy path - Chefia acessa detalhes de subordinado da mesma lotação
- [x] 2.3 Escrever pytest: teste permissão - Chefia não acessa usuário de outra lotação (403)
- [x] 2.4 Escrever pytest: teste permissão - Trabalhador não acessa detalhes (403)
- [x] 2.5 Escrever pytest: teste usuário não encontrado (404)
- [x] 2.6 Executar `pytest tests/test_usuario_detalhes_endpoint.py` e verificar todos passando (11 tests passed)

## 3. Frontend - Componente UserDetailsModal

- [x] 3.1 Criar componente `frontend/src/components/UserDetailsModal.vue` com props `show` (boolean) e `userId` (string)
- [x] 3.2 Implementar chamada API para `GET /api/relatorios/usuario/{userId}/detalhes` no componente
- [x] 3.3 Exibir DataTable com cursos, status, certificados do usuário (reutilizar headers de `RelatoriosChefia.vue`)
- [x] 3.4 Adicionar estados de loading e erro no modal
- [x] 3.5 Adicionar link para visualizar certificado quando disponível (reutilizar `getCertificateUrl`)

## 4. Frontend - Tests - UserDetailsModal

- [x] 4.1 Escrever vitest em `frontend/src/components/UserDetailsModal.test.ts`: teste rendering - modal fechado por padrão
- [x] 4.2 Escrever vitest: teste user interaction - abrir modal carrega dados do usuário via API
- [x] 4.3 Escrever vitest: teste error handling - exibe mensagem de erro quando API falha
- [x] 4.4 Executar `npx vitest run` e verificar todos passando (6 tests passed)

## 5. Frontend - RelatoriosCapacitacoes.vue (UDP)

- [x] 5.1 Importar e integrar `UserDetailsModal` em `RelatoriosCapacitacoes.vue`
- [x] 5.2 Adicionar slot `#item-nome_profissional` no DataTable com link clicável no nome
- [x] 5.3 Implementar handler `openUserDetails(userId)` que extrai o user_id dos dados e abre o modal
- [x] 5.4 Ajustar dados da API para incluir `id` do usuário (ver backend task 7.1)

## 6. Frontend - RelatorioConsolidado.vue (Chefia e UDP)

- [x] 6.1 Importar e integrar `UserDetailsModal` em `RelatorioConsolidado.vue`
- [x] 6.2 Adicionar slot `#item-nome` no DataTable com link clicável no nome
- [x] 6.3 Implementar handler para abrir modal de detalhes do usuário
- [x] 6.4 Ajustar dados da API para incluir `id` do usuário no relatório consolidado (backend task 7.2)

## 7. Backend - Incluir user_id nos relatórios

- [x] 7.1 Adicionar `Usuario.id` ao retorno de `listar_dados_capacitacoes` no `RelatorioProvider` (provider)
- [x] 7.2 Adicionar `Usuario.id` ao retorno de `get_relatorio_consolidado` no controller
- [x] 7.3 Verificar que os dados retornados pela API incluem `id` em cada registro

## 8. Frontend - Tests - Views integradas

- [x] 8.1 Escrever vitest em `frontend/src/views/RelatoriosCapacitacoes.test.ts`: teste que nome do profissional é renderizado como link
- [x] 8.2 Escrever vitest em `frontend/src/views/RelatorioConsolidado.test.ts`: teste que nome é renderizado como link e abre modal ao clicar
- [x] 8.3 Executar `npx vitest run` e verificar todos passando (4 tests passed)

## 9. Integração e verificação final

- [x] 9.1 Testar manualmente: UDP clica em nome no relatório de Capacitações e vê detalhes
- [x] 9.2 Testar manualmente: Chefia clica em nome no relatório Consolidado e vê detalhes
- [x] 9.3 Testar manualmente: UDP clica em nome no relatório Consolidado e vê detalhes
- [x] 9.4 Executar `pytest` completo e verificar sem falhas (41 passed)
- [x] 9.5 Executar `npx vitest run` completo e verificar sem falhas (23 passed)
