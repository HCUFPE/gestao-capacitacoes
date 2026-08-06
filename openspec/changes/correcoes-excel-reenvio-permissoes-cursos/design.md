## Context

Três necessidades foram reportadas:
1. Erro 500 na exportação Excel do Relatório Consolidado Chefia devido à falta de pacote de escrita Excel em Python.
2. Impossibilidade de reenviar certificado caso o envio inicial tenha sido incorreto em cursos com status `Realizado` ou `Recusado`.
3. Garantia de restrição nas operações de cursos (criação, edição, exclusão) apenas para `Chefia` e `UDP`.

## Goals / Non-Goals

**Goals:**
- Incluir `xlsxwriter` e `openpyxl` no `requirements.txt` e ambiente virtual.
- Atualizar a exibição do botão "Reenviar Certificado" em `MeusCursos.vue` para status `Realizado` e `Recusado`.
- Validar as regras de acesso das rotas de gestão de cursos.

**Non-Goals:**
- Alterar a lógica de permissões gerais de usuários além das já definidas.

## Decisions

- **Decisão 1: Dependência de Excel**: Adicionar `xlsxwriter` ao `requirements.txt` para que o `pandas.ExcelWriter(..., engine='xlsxwriter')` funcione sem erros.
- **Decisão 2: Filtro de Status para Reenvio**: Ajustar as condições `v-if` dos botões de ação em `MeusCursos.vue` para exibir "Reenviar" para os status `Realizado` e `Recusado`, e omitir para `Validado` e `Concluído` (evitando erro 400).
- **Decisão 3: Manutenção de Guards**: Manter os endpoints de `src/routers/curso.py` protegidos por `is_chefia` (que já aceita tanto Chefia quanto UDP).
