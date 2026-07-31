## 1. Database Fixes

- [x] 1.1 Run Alembic migrations on local SQLite database to apply missing columns (`alembic upgrade head`)
- [x] 1.2 Verify if `atribuicoes` table successfully updated with `data_atribuicao` and `data_validacao`. If it fails due to SQLite constraints, manually recreate the local database or adjust the migration for SQLite compatibility.

## 2. Testing and Verification

- [x] 2.1 Start the backend server and ensure no errors are thrown when querying pending tasks.
- [x] 2.2 Validate that the certificate validation page works on the frontend without returning 500 or OperationalError.
- [x] 2.3 Run backend test suite (`pytest`) to ensure no regressions in test coverage for `atribuicao_controller.py`.
