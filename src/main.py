from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os
import traceback
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

from .resources.database import DatabaseManager
from .models.base import Base
from .models import * # Import all models for SQLAlchemy to discover

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")


    # Initialize AGHU DB Manager and store in app.state
    aghu_dsn = os.getenv("POSTGRES_DSN")
    if aghu_dsn:
        app.state.aghu_db = DatabaseManager(aghu_dsn)
        print("AGHU PostgreSQL connection pool initialized.")
    else:
        print("WARNING: POSTGRES_DSN not found. Skipping AGHU DB initialization.")

    # Initialize App DB Manager (SQLite) and store in app.state
    app_dsn = os.getenv("SQLITE_DSN")
    if not app_dsn:
        raise ValueError("SQLITE_DSN not found in environment variables.")
    app.state.app_db = DatabaseManager(app_dsn)
    print("App SQLite connection pool initialized.")

    # Create tables for App DB (if they don't exist) - for development only, Alembic handles this in production
    async with app.state.app_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("App SQLite tables checked/created.")

    yield

    # Shutdown
    print("Shutting down...")
    if hasattr(app.state, 'aghu_db') and app.state.aghu_db:
        await app.state.aghu_db.close_connection()
        print("AGHU PostgreSQL connection pool closed.")
    if hasattr(app.state, 'app_db') and app.state.app_db:
        await app.state.app_db.close_connection()
        print("App SQLite connection pool closed.")

app = FastAPI(
    title="Esqueleto de Aplicação Web Full-Stack",
    description="Aplicação Backend monolítica (API REST) em Python/FastAPI, com foco em acesso e agregação de dados heterogêneos.",
    version="1.0.0",
    lifespan=lifespan,
)

# Adiciona o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

@app.middleware("http")
async def detailed_error_middleware(request: Request, call_next):
    """
    Middleware to catch unhandled exceptions and log them with details.
    """
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print("--- Unhandled Exception ---")
        print(f"Request: {request.method} {request.url}")
        print("Headers:")
        for name, value in request.headers.items():
            print(f"  {name}: {value}")
        
        print("\nTraceback:")
        traceback.print_exc()
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": str(e),
                "traceback": traceback.format_exc(),
            },
        )

# Serve o frontend Vue 3 empacotado
app.mount("/assets", StaticFiles(directory="src/static/dist/assets"), name="assets")

# Placeholder para incluir os roteadores da API
from .routers import auth, admin, curso, certificado, relatorio, atribuicao, utils, inscricao
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(curso.router)
app.include_router(certificado.router)
app.include_router(relatorio.router)
app.include_router(atribuicao.router)
app.include_router(utils.router)
app.include_router(inscricao.router)

# Exemplo:
# from .routers import aih, bpa, material
# app.include_router(aih.router)
# app.include_router(bpa.router)
# app.include_router(material.router)

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """
    Serve o arquivo index.html do frontend Vue para qualquer rota não correspondida pela API.
    Isso é essencial para o roteamento do lado do cliente (Vue Router) funcionar corretamente.
    """
    return FileResponse(os.path.join("src", "static", "dist", "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
