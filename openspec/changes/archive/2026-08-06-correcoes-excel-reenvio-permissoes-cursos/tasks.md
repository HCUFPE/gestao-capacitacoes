## 1. Exportação Excel & Dependências

- [x] 1.1 Adicionar `xlsxwriter` e `openpyxl` ao arquivo `requirements.txt` e instalar no ambiente virtual.
- [x] 1.2 Escrever teste automatizado Pytest em `tests/test_relatorio_consolidado_filtro.py` para validar a exportação Excel em `/api/relatorios/chefia/consolidado/export/excel`.

## 2. Interface de Reenvio de Certificados

- [x] 2.1 Atualizar `frontend/src/views/MeusCursos.vue` para exibir o botão "Reenviar Certificado" em cursos com status `Realizado` e `Recusado`.
- [x] 2.2 Escrever testes automatizados Vitest em `frontend/src/views/MeusCursos.test.ts` cobrindo o acionamento de reenvio de certificado para o status `Realizado`.

## 3. Controle de Acesso e Permissões de Cursos

- [x] 3.1 Verificar e validar a proteção das rotas de curso em `src/routers/curso.py` garantindo acesso restrito a `Chefia` ou `UDP`.
- [x] 3.2 Executar suíte de testes de rotas e permissões para confirmar bloqueio a perfis não autorizados.
