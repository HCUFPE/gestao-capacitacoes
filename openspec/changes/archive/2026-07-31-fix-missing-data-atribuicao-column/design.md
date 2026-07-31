## Context

The `Atribuicao` model specifies columns `data_atribuicao` and `data_validacao`. An Alembic migration (`a1b2c3d4e5f6_add_data_atribuicao_and_data_validacao_.py`) was created to add these columns. However, when querying the SQLite database locally to view pending items or validate a certificate, an `OperationalError` occurs: `no such column: atribuicoes.data_atribuicao`.
This suggests the migration has not been run or did not correctly execute on SQLite (which has limited `ALTER TABLE` support, though Alembic's `batch_op` with `add_column` usually works for `DateTime`). We need to fix the database schema locally.

## Goals / Non-Goals

**Goals:**
- Fix the `OperationalError` regarding the missing `data_atribuicao` (and `data_validacao`) columns on the local SQLite database.
- Make the certificate validation page load successfully without errors.

**Non-Goals:**
- Modifications to Oracle or PostgreSQL databases (assuming they are already correct or handled separately).
- Changes to the frontend or application logic.

## Decisions

- Run Alembic migrations up to head (`alembic upgrade head`) to ensure the SQLite schema is up to date.
- Verify if the `a1b2c3d4e5f6` migration applied correctly to the local `capacitacoes.db` or if the DB file needs to be deleted and recreated. If recreating is needed, drop all tables and let alembic re-run all migrations from scratch.

## Risks / Trade-offs

- **Risk:** Deleting the local SQLite DB will erase local mock data.
  **Mitigation:** Only delete the database if running migrations directly fails. Since it's a local development database, losing data is usually acceptable, and it can be recreated.
