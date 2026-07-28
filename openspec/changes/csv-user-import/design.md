## Context

Atualmente, o processo de importação de usuários é realizado via script CLI `import_users.py`. A lógica de processamento lê o arquivo CSV/query SQL, valida as colunas e atualiza/insere no banco via SQLAlchemy `AsyncSession`. Para disponibilizar essa funcionalidade via Web, precisamos extrair a lógica de negócio reutilizável de importação de CSV para a camada de controller (`src/controllers/usuario_controller.py` ou módulo utilitário) e expô-la em um endpoint REST seguro com FastAPI, além de criar a interface gráfica correspondente em Vue 3.

## Goals / Non-Goals

**Goals:**
- Desacoplar a lógica de parse e persistência do CSV em uma função auxiliar/controller reutilizável tanto pela CLI quanto pela API HTTP.
- Criar o endpoint `POST /admin/usuarios/importar-csv` utilizando `UploadFile` e restrição de permissão `is_udp`.
- Desenvolver componente Vue 3 para seleção do arquivo CSV com exibição de resultados em tempo real (modal ou card na view de administração).
- Garantir 100% de cobertura com testes automatizados no backend (`pytest`) e frontend (`vitest`).

**Non-Goals:**
- Alterar o esquema de dados do modelo `Usuario`.
- Implementar importação assíncrona com filas (Celery/Redis), mantendo o processamento síncrono para o upload via requisição HTTP dado a volumetria média de usuários.

## Decisions

- **Decisão 1: Reutilização da Lógica de Importação**:
  - Extrair a função `process_csv_user_data(file_content_or_stream, db)` em um serviço/controller (`src/controllers/usuario_controller.py`).
  - *Alternativa considerada*: Duplicar o código do script `import_users.py` no endpoint. Descartada para evitar código duplicado e inconsistências de manutenção.
- **Decisão 2: Endpoint FastAPI com `UploadFile`**:
  - O endpoint utilizará `UploadFile = File(...)` e validará o Content-Type/extensão `.csv`.
  - Retorno da API: `{ "sucesso": true, "novos": X, "atualizados": Y, "erros": [...] }`.
- **Decisão 3: Interface no Frontend**:
  - Criar o componente `ImportUsuariosModal.vue` e integrá-lo à view de gerenciamento de usuários.
  - Usar serviço `adminService.importarUsuariosCsv(file: File)`.

## Risks / Trade-offs

- [Arquivos CSV grandes gerando timeout HTTP] → Definir limite razonável de tamanho no upload (ex: 5MB ou 10.000 registros) e processamento em lote (batching) na sessão do SQLAlchemy.
- [Codificação de caracteres (UTF-8 vs Latin-1/ISO-8859-1)] → Fazer a leitura tentando UTF-8 com fallback gracioso para Latin-1.
