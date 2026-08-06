## Why

1. **Erro 500 na Exportação de Excel**: A exportação do Relatório Consolidado para Excel gerava erro HTTP 500 no backend devido à falta do pacote `xlsxwriter` / `openpyxl` na inicialização do `pandas.ExcelWriter`.
2. **Reenvio de Certificado**: Usuários que enviaram certificados incorretos não encontravam a opção para reenviar/substituir o arquivo nos cursos com status `Realizado` ou `Recusado`.
3. **Restrição de Permissões de Cursos**: Garantir que as rotas e ações de criação, edição e exclusão de cursos estejam restritas aos perfis `CHEFIA` e `UDP`.

## What Changes

- **Dependência de Excel**: Adicionar `xlsxwriter` e `openpyxl` ao `requirements.txt` e garantir o suporte nativo à exportação de planilhas no backend.
- **Reenvio na Interface**: Exibir o botão "Reenviar Certificado" nas visões de card de `MeusCursos.vue` para atribuições nos status `Realizado` e `Recusado`.
- **Verificação de Permissões**: Manter a proteção de rotas de gestão de cursos (`/api/cursos` e `/gestao-cursos`) restritas exclusivamente a `Chefia` e `UDP`.

## Capabilities

### New Capabilities
- `correcao-export-excel-reenvio-permissoes`: Ajuste na exportação Excel (500), botão de reenvio de certificados e controle de acesso para cursos.

### Modified Capabilities

## Impact

- **Backend**: `requirements.txt`, `src/helpers/excel_helper.py`, `src/routers/curso.py`.
- **Frontend**: `frontend/src/views/MeusCursos.vue`, `frontend/src/components/CourseDetailsModal.vue`.
- **Testes**: Testes automatizados Pytest e Vitest.
