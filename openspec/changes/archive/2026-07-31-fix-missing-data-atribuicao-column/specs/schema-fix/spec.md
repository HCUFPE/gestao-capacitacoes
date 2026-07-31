## ADDED Requirements

### Requirement: Database Schema Integrity
The system SHALL ensure the local SQLite database schema matches the expected SQLAlchemy models.

#### Scenario: SQLite Schema Consistency
- **WHEN** the system queries the SQLite database for pending `atribuicoes`
- **THEN** it completes successfully without `OperationalError` regarding missing columns
