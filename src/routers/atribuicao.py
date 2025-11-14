from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from datetime import datetime

from ..controllers import atribuicao_controller
from ..auth.auth import auth_handler
from ..auth.dependencies import get_current_user
from ..resources.database import get_app_db_session
from ..models import StatusAtribuicao

# --- Pydantic Schemas for Response ---

class CursoForAtribuicaoResponse(BaseModel):
    id: str
    titulo: str
    carga_horaria: int | None = None
    ano_gd: str | None = None
    link: str | None = None

    class Config:
        from_attributes = True

class AtribuicaoResponse(BaseModel):
    id: str
    status: StatusAtribuicao
    atribuido_em: datetime
    curso: CursoForAtribuicaoResponse

    class Config:
        from_attributes = True

# --- Router Definition ---

router = APIRouter(
    prefix="/api/atribuicoes",
    tags=["Atribuições"],
)

@router.get("/me", response_model=List[AtribuicaoResponse], dependencies=[Depends(auth_handler.decode_token)])
async def listar_minhas_atribuicoes(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Lista todas as atribuições de cursos para o usuário logado.
    """
    user_id = current_user.get("sub") # 'sub' é o sAMAccountName no nosso token
    return await atribuicao_controller.listar_atribuicoes_por_usuario(db, user_id)
