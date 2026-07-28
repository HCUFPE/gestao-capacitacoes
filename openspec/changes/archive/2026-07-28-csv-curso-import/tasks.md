## 1. Backend Implementation

- [x] 1.1 Implementar a função `importar_cursos_csv(file_bytes, db)` em `src/controllers/curso_controller.py` com parsing de `;`, fallback de encoding (`utf-8` / `iso-8859-1`) e mapeamento para o modelo `Curso`.
- [x] 1.2 Implementar lógica de Upsert (atualizar se `id_curso` existir; inserir se não existir) retornando resumo com contadores de novos, atualizados e erros.
- [x] 1.3 Criar a rota `POST /cursos/importar-csv` em `src/routers/curso.py` (ou `admin.py`) aceitando `UploadFile` e protegida com verificação de perfil de administração.
- [x] 1.4 Criar suíte de testes em `tests/test_curso_csv_import.py` cobrindo o envio de CSV com delimitador `;`, encoding `iso-8859-1`, upsert de cursos novos e existentes, e erros de validação.

## 2. Frontend Implementation

- [x] 2.1 Adicionar a função `importarCursosCsv(file: File)` no serviço `cursoService.ts` / `adminService.ts`.
- [x] 2.2 Criar o componente `ImportCursosModal.vue` com seletor de arquivo `.csv`, barra/spinner de carregamento e exibição formatada do resumo (novos, atualizados, erros).
- [x] 2.3 Adicionar o botão "Importar Cursos (CSV)" na tela de gerenciamento de cursos/catálogo.
- [x] 2.4 Criar testes de componente no Vitest em `frontend/src/components/ImportCursosModal.test.ts` cobrindo upload do arquivo e renderização das mensagens de sucesso/erro.
