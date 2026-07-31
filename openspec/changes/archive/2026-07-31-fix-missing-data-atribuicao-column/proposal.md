## Why

The system throws an `OperationalError: no such column: atribuicoes.data_atribuicao` when trying to fetch pending certificate validations or tasks, because the SQLite database schema does not match the SQLAlchemy models. This prevents users from validating certificates.

## What Changes

- Apply the existing Alembic migrations to the local SQLite database to ensure the `atribuicoes` table has the `data_atribuicao` and `data_validacao` columns.
- Ensure the database schema matches the expected models.
- If migrations are failing for SQLite, fix the migration script to correctly handle schema modifications in SQLite.

## Capabilities

### New Capabilities
<!-- Capabilities being introduced. Replace <name> with kebab-case identifier (e.g., user-auth, data-export, api-rate-limiting). Each creates specs/<name>/spec.md -->

### Modified Capabilities
<!-- Existing capabilities whose REQUIREMENTS are changing (not just implementation).
     Only list here if spec-level behavior changes. Each needs a delta spec file.
     Use existing spec names from openspec/specs/. Leave empty if no requirement changes. -->

## Impact

- Database schema for `atribuicoes` table.
- Certificate validation flow (will be functional).
