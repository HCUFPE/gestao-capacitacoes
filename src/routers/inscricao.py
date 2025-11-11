from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from datetime import datetime

from ..controllers import inscricao_controller
from ..auth.auth import auth_handler
from ..auth.dependencies import get_current_user
from ..resources.database import get_app_db_session

# --- Pydantic Schemas for Request/Response ---

class CursoForInscricaoResponse(BaseModel):
    id: str
    titulo: str
    certificadora: str | None = None
    carga_horaria: int | None = None
    link: str | None = None
    ano_gd: str | None = None # AnoGD enum is converted to string for response

    class Config:
        from_attributes = True

class InscricaoResponse(BaseModel):
    id: str
    usuario_id: str
    curso_id: str
    data_inscricao: datetime
    curso: CursoForInscricaoResponse

    class Config:
        from_attributes = True

class InscricaoCreate(BaseModel):
    curso_id: str

# --- Router Definition ---

router = APIRouter(
    prefix="/api/inscricoes",
    tags=["Inscrições"],
    dependencies=[Depends(auth_handler.decode_token)]
)

@router.post("/", response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
async def inscrever_em_curso(
    inscricao_data: InscricaoCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Permite que o usuário logado se inscreva em um curso.
    """
    usuario_id = current_user.get("sub")
    
    # Verificar se a inscrição já existe
    existing_inscricao = await inscricao_controller.verificar_inscricao_existente(db, usuario_id, inscricao_data.curso_id)
    if existing_inscricao:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Usuário já inscrito neste curso."
        )

    return await inscricao_controller.inscrever_usuario_em_curso(db, usuario_id, inscricao_data.curso_id)

@router.delete("/{inscricao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def desinscrever_de_curso(
    inscricao_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Permite que o usuário logado se desinscreva de um curso.
    """
    # Verificar se a inscrição pertence ao usuário logado antes de deletar
    inscricoes = await inscricao_controller.listar_inscricoes_por_usuario(db, current_user.get("sub"))
    if not any(insc.id == inscricao_id for insc in inscricoes):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para desinscrever-se deste curso."
        )

    success = await inscricao_controller.desinscrever_usuario_de_curso(db, inscricao_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada.")
    return

@router.get("/me", response_model=List[InscricaoResponse])
async def listar_minhas_inscricoes(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Lista todas as inscrições do usuário logado.
    """
    usuario_id = current_user.get("sub")
    return await inscricao_controller.listar_inscricoes_por_usuario(db, usuario_id)
