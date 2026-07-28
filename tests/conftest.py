"""
Shared fixtures and configuration for the entire test suite.
"""
import asyncio
import os
from typing import AsyncGenerator
import pytest
from httpx import ASGITransport, AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Ensure the project root is on sys.path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.models.base import Base
from src.resources.database import DatabaseManager

# Use an in-memory SQLite database for tests
TEST_DSN = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db() -> AsyncGenerator[DatabaseManager, None]:
    """
    Creates an in-memory SQLite database with all tables.
    Yields the DatabaseManager and tears down after each test.
    """
    engine = create_async_engine(TEST_DSN, echo=False)
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield SessionLocal

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(test_db) -> AsyncGenerator[AsyncSession, None]:
    """Provides an isolated async session for each test, auto-rolled-back."""
    async with test_db() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def app():
    """
    Creates a test FastAPI app with an in-memory SQLite database.
    """
    os.environ.setdefault("SQLITE_DSN", TEST_DSN)

    from src.main import app
    from src.resources.database import DatabaseManager

    # Replace the app's DB manager with the test one
    test_manager = DatabaseManager(TEST_DSN)
    app.state.app_db = test_manager

    # Create tables
    async with test_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield app

    await test_manager.close_connection()


@pytest.fixture
async def async_client(app) -> AsyncGenerator[AsyncClient, None]:
    """Provides an async HTTP client against the test app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def test_user_data():
    """Sample user data for creating test users."""
    return {
        "id": "test-user-001",
        "nome": "Usuário Teste",
        "perfil": "TRABALHADOR",
        "lotacao": "teste-lotacao",
        "matricula": "123456",
        "cargo": "Analista",
        "cpf": "12345678900",
    }


@pytest.fixture
def test_curso_data():
    """Sample curso data for creating test cursos."""
    return {
        "id": "test-curso-001",
        "titulo": "Curso de Teste",
        "carga_horaria": 40,
        "ano_gd": "2025",
        "lotacao_id": "teste-lotacao",
        "certificadora": "Test Corp",
        "link": "https://example.com/curso",
    }


@pytest.fixture
def test_certificado_data():
    """Sample certificado data."""
    return {
        "id": "test-cert-001",
        "curso_id": "test-curso-001",
        "file_path": "/path/to/cert.pdf",
        "link": "https://example.com/cert",
    }
