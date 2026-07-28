## Context

O catálogo de cursos da aplicação é mantido no modelo `Curso` (`src/models/curso.py`). O objetivo deste desenho técnico é permitir o upload e processamento do arquivo `capacitacao.csv` no backend (FastAPI) e frontend (Vue 3), realizando a leitura com tratamento de encodings (`ISO-8859-1` / `UTF-8`) e delimitador `;`.

## Goals / Non-Goals

**Goals:**
- Implementar a função `importar_cursos_csv(file_bytes, db)` em `src/controllers/curso_controller.py`.
- Suportar o parsing de CSV estruturado com `;` e mapear colunas para os atributos da tabela `cursos`.
- Garantir comportamento idempotente (Upsert): registros com `id_curso` já existente serão atualizados (`UPDATE`); registros novos serão criados (`INSERT`).
- Criar endpoint `POST /cursos/importar-csv` em `src/routers/curso.py` (ou `admin.py`).
- Implementar componente `ImportCursosModal.vue` no frontend.
- Escrever testes automatizados backend (`pytest`) e frontend (`vitest`).

**Non-Goals:**
- Excluir cursos do banco de dados que não estiverem presentes na planilha enviada (a importação é acumulativa/incremental).

## Decisions

- **Decisão 1: Leitura com `csv.DictReader` e detecção/fallback de encoding**:
  - Tentar decodificar os bytes do arquivo em `utf-8`. Se falhar com `UnicodeDecodeError`, aplicar `iso-8859-1`.
  - Usar `csv.DictReader(stream, delimiter=';')`.
- **Decisão 2: Mapeamento Explícito de Colunas**:
  ```python
  COLUMN_MAP = {
      'id_curso': 'id',
      'nome_curso': 'titulo',
      'Link': 'link',
      'eixos_tematicos': 'tema',
      'certificador': 'certificadora',
      'conteudista': 'conteudista',
      'carga_horaria': 'carga_horaria',
      'disponibilidade_dias': 'disponibilidade_dias',
      'tipo_oferta': 'tipo_oferta',
      'apresentacao': 'apresentacao',
      'publico_alvo': 'publico_alvo',
      'conteudo_programatico': 'conteudo_programatico',
      'data_lancamento': 'data_lancamento',
      'Acessibilidade': 'acessibilidade',
      'Observacao': 'observacao'
  }
  ```
- **Decisão 3: Upsert em Sessão Async (SQLAlchemy)**:
  - Para cada linha, buscar `Curso` por `id`. Se existir, atualizar atributos; se não, instanciar `Curso(...)` e adicionar à sessão. Fazer commit no final do lote.

## Risks / Trade-offs

- [Valores vazios de carga horária / disponibilidade em formato texto] → Converter com try/except para `int` seguro, atribuindo `None` se a célula estiver em branco.
- [Arquivos com delimitador `,` em vez de `;`] → Validar o cabeçalho na primeira linha do CSV antes de iterar.
