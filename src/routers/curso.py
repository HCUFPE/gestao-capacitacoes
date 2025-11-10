from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel

from ..controllers import curso_controller
from ..auth.auth import auth_handler
from ..resources.database import get_app_db_session
from ..models import Curso, AnoGD

from ..auth.dependencies import is_chefia

# --- Pydantic Schemas for Request/Response ---

class CursoBase(BaseModel):
    titulo: str
    certificadora: str | None = None
    carga_horaria: int | None = None
    link: str | None = None
    ano_gd: AnoGD | None = None
    chefia_id: str
    lotacao: str

class CursoCreate(CursoBase):
    pass

class CursoResponse(CursoBase):
    id: str

    class Config:
        from_attributes = True

# --- Router Definition ---

router = APIRouter(
    prefix="/api/cursos",
    tags=["Cursos"],
)

@router.get("/", response_model=List[CursoResponse], dependencies=[Depends(auth_handler.decode_token)])
async def listar_cursos(
    db: AsyncSession = Depends(get_app_db_session)
):
    """Lista todos os cursos da fonte de dados interna."""
    return await curso_controller.listar_cursos(db)

@router.post("/", response_model=CursoResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth_handler.decode_token), Depends(is_chefia)])
async def criar_curso(
    curso: CursoCreate,
    db: AsyncSession = Depends(get_app_db_session)
):
    """Cria um novo curso na fonte de dados interna. (Requer perfil de Chefia ou UDP)"""
    return await curso_controller.criar_curso(db, curso.dict())

@router.put("/{curso_id}", response_model=CursoResponse, dependencies=[Depends(auth_handler.decode_token), Depends(is_chefia)])
async def atualizar_curso(
    curso_id: str,
    curso: CursoCreate,
    db: AsyncSession = Depends(get_app_db_session)
):
    """Atualiza um curso existente. (Requer perfil de Chefia ou UDP)"""
    updated_curso = await curso_controller.atualizar_curso(db, curso_id, curso.dict())
    if updated_curso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    return updated_curso

@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth_handler.decode_token), Depends(is_chefia)])
async def deletar_curso(
    curso_id: str,
    db: AsyncSession = Depends(get_app_db_session)
):
    """Deleta um curso e suas atribuições. (Requer perfil de Chefia ou UDP)"""
    success = await curso_controller.deletar_curso(db, curso_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    return

@router.get("/{curso_id}", response_model=CursoResponse, dependencies=[Depends(auth_handler.decode_token)])
async def obter_curso(
    curso_id: str,
    db: AsyncSession = Depends(get_app_db_session)
):
    """Obtém um curso pelo ID a partir da fonte de dados interna."""
    curso = await curso_controller.obter_curso_por_id(db, curso_id)
    if curso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    return curso
