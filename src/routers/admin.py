from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List

from ..auth.dependencies import is_udp
from ..resources.database import get_app_db_session
from ..controllers import usuario_controller
from ..models import PerfilUsuario, Usuario

# --- Pydantic Schemas ---

class PerfilUpdateRequest(BaseModel):
    user_id: str
    novo_perfil: PerfilUsuario

class UserProfileResponse(BaseModel):
    id: str
    nome: str
    email: str | None = None
    perfil: PerfilUsuario
    lotacao: str | None = None
    course_count: int = 0

    class Config:
        from_attributes = True

# --- Router Definition ---

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
)

@router.put("/usuarios/perfil", response_model=UserProfileResponse, dependencies=[Depends(is_udp)])
async def atualizar_perfil_usuario(
    request: PerfilUpdateRequest,
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Atualiza o perfil de um usuário. (Requer perfil de UDP)
    """
    updated_user = await usuario_controller.atualizar_perfil_usuario(
        db=db,
        user_id=request.user_id,
        novo_perfil=request.novo_perfil
    )
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return updated_user

@router.get("/usuarios", response_model=List[UserProfileResponse], dependencies=[Depends(is_udp)])

async def listar_todos_usuarios(

    nome: str | None = None,

    lotacao: str | None = None,

    db: AsyncSession = Depends(get_app_db_session)

):

    """

    Lista todos os usuários cadastrados no sistema, com filtros opcionais. 

    (Requer perfil de UDP)

    """

    return await usuario_controller.listar_usuarios(db, nome=nome, lotacao=lotacao)
