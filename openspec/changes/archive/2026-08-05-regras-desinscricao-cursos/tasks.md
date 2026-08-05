## 1. Alterações no Frontend

- [x] 1.1 Atualizar `frontend/src/views/MeusCursos.vue` para exibir o botão de desinscrição apenas quando `inscricao.status === 'Em Andamento'`.
- [x] 1.2 Criar/atualizar testes unitários no Vitest para validar a exibição condicional do botão de desinscrição.

## 2. Validações no Backend

- [x] 2.1 Adicionar trava de segurança em `src/controllers/inscricao_controller.py` recusando a desinscrição de registros com certificado anexado.
- [x] 2.2 Criar/atualizar testes do Pytest para validar o bloqueio do backend ao tentar excluir inscrição com certificado.
