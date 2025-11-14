from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel

from ..auth.auth import auth_handler
from ..resources.database import get_app_db_session
from ..controllers import usuario_controller, dashboard_controller

router = APIRouter(
    prefix="/api/utils",
    tags=["Utilities"],
)

class DashboardStatsResponse(BaseModel):
    total_cursos: int
    total_inscricoes: int
    total_certificados_validados: int
    total_usuarios: int

@router.get("/lotacoes", response_model=List[str], dependencies=[Depends(auth_handler.decode_token)])
async def get_lotacoes_unicas(
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Retorna uma lista de todas as lotações (setores) únicas cadastradas no sistema.
    """
    return await usuario_controller.listar_lotacoes_unicas(db)

@router.get("/stats", response_model=DashboardStatsResponse, dependencies=[Depends(auth_handler.decode_token)])
async def get_stats(
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Retorna estatísticas gerais para o dashboard.
    """
    return await dashboard_controller.get_dashboard_stats(db)
