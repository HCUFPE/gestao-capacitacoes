from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from datetime import datetime

from ..controllers import atribuicao_controller, usuario_controller
from ..auth.auth import auth_handler
from ..auth.dependencies import get_current_user, is_chefia
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

class AtribuicaoPendenteResponse(BaseModel):
    atribuicao_id: str
    data_submissao: datetime
    usuario_nome: str
    curso_titulo: str
    certificado_id: str | None = None

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

@router.get("/pendentes-validacao", response_model=List[AtribuicaoPendenteResponse], dependencies=[Depends(is_chefia)])
async def get_atribuicoes_pendentes_validacao(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    (Chefia) Lista as atribuições com certificados submetidos que aguardam validação.
    """
    user_id = current_user.get("sub")
    user = await usuario_controller.get_user_by_username(db, user_id)
    
    if not user or not user.lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")
        
    return await atribuicao_controller.listar_atribuicoes_pendentes_validacao(db, user.lotacao)
