from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from datetime import datetime

from ..controllers import atribuicao_controller, usuario_controller
from ..auth.auth import auth_handler
from ..auth.dependencies import get_current_user, is_chefia
from ..resources.database import get_app_db_session
from ..models import StatusAtribuicao, Usuario
from sqlalchemy import select

# --- Pydantic Schemas for Response ---

class CursoForAtribuicaoResponse(BaseModel):
    id: str
    titulo: str
    certificadora: str | None = None
    carga_horaria: int | None = None
    ano_gd: str | None = None
    link: str | None = None
    lotacao_id: str | None = None

    class Config:
        from_attributes = True

class AtribuicaoResponse(BaseModel):
    id: str
    user_id: str | None = None
    curso_id: str | None = None
    status: StatusAtribuicao
    atribuido_em: datetime
    certificado_id: str | None = None
    certificado_file_path: str | None = None
    certificado_link: str | None = None
    curso: CursoForAtribuicaoResponse

    class Config:
        from_attributes = True

class AtribuicaoPendenteResponse(BaseModel):
    atribuicao_id: str
    data_submissao: datetime
    usuario_nome: str
    curso_titulo: str
    certificado_id: str | None = None


class GranularAtribuicaoRequest(BaseModel):
    curso_id: str
    user_ids: List[str]


class LotacaoUserResponse(BaseModel):
    id: str
    nome: str
    email: str | None = None
    lotacao: str | None = None

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


@router.post("/lotacao", dependencies=[Depends(is_chefia)])
async def atribuir_curso_seletivo(
    request: GranularAtribuicaoRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    (Chefia) Atribui um curso a usuários específicos da própria lotação.
    Valida que cada usuário pertence à lotação da chefia.
    Ignora duplicações silenciosamente.
    """
    user_id = current_user.get("sub")
    user = await usuario_controller.get_user_by_username(db, user_id)

    if not user or not user.lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")

    if not request.user_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lista de usuários vazia.")

    try:
        count = await atribuicao_controller.criar_atribuicoes_seletivas(
            db, request.curso_id, request.user_ids, user.lotacao
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    return {"message": f"{count} atribuição(ões) criada(s) com sucesso.", "count": count}


@router.get("/lotacao/usuarios", response_model=List[LotacaoUserResponse], dependencies=[Depends(is_chefia)])
async def listar_usuarios_lotacao_chefia(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    (Chefia) Lista todos os usuários da própria lotação.
    """
    user_id = current_user.get("sub")
    user = await usuario_controller.get_user_by_username(db, user_id)

    if not user or not user.lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")

    stmt = (
        select(Usuario.id, Usuario.nome, Usuario.email, Usuario.lotacao)
        .where(Usuario.lotacao == user.lotacao)
        .order_by(Usuario.nome)
    )
    result = await db.execute(stmt)
    rows = result.mappings().all()
    return [
        {
            "id": row["id"],
            "nome": row["nome"],
            "email": row["email"],
            "lotacao": row["lotacao"],
        }
        for row in rows
    ]
