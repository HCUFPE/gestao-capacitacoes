## Why

O catálogo de cursos e capacitações precisa ser atualizado periodicamente com base em planilhas disponibilizadas por órgãos parceiros e plataformas de ensino (ex: Escola Virtual Gov, Ebserh, Enap). Atualmente, a adição e atualização massiva de cursos requer manipulação direta do banco de dados ou cadastros individuais pela API. Disponibilizar o upload da planilha `capacitacao.csv` permitirá que os administradores atualizem e expandam o catálogo de cursos de forma automática, ágil e idempotente.

## What Changes

- **Endpoint de Importação de Cursos via CSV**: Criar `POST /admin/cursos/importar-csv` (ou `POST /cursos/importar-csv`) aceitando upload de arquivo CSV via `multipart/form-data`.
- **Parsing e Upsert de Cursos**: Suporte a arquivos codificados em `ISO-8859-1` ou `UTF-8`, com delimitador `;` (ponto e vírgula), mapeando as colunas da planilha `capacitacao.csv` para os atributos do modelo `Curso` (`id_curso` ➔ `id`, `nome_curso` ➔ `titulo`, `Link` ➔ `link`, `eixos_tematicos` ➔ `tema`, etc.).
- **Logica de Upsert Incremental**: Se o `id_curso` já existir no banco, atualiza os dados sem duplicar; se não existir, insere como novo curso.
- **Interface Frontend (Vue 3)**: Adicionar botão e modal de upload de planilha de capacitações na gestão de cursos/administração, exibindo progresso e relatório final (novos cursos cadastrados, cursos atualizados e possíveis erros).

## Capabilities

### New Capabilities
- `csv-curso-import`: Capacidade de realizar carga e atualização massiva do catálogo de cursos via arquivo CSV (`capacitacao.csv`) com suporte a upsert e feedback detalhado.

### Modified Capabilities
<!-- Nenhuma modificação de requisitos em capabilities existentes -->

## Impact

- **Backend**: Adição de endpoint em `src/routers/curso.py` ou `src/routers/admin.py`, lógica de negócio em `src/controllers/curso_controller.py`.
- **Frontend**: Inclusão de modal/componente de importação de cursos e integração no serviço `cursoService.ts` / `adminService.ts`.
- **Banco de Dados**: Operações de `UPDATE` e `INSERT` na tabela `cursos`.
