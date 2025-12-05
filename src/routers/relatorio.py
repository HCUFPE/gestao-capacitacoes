from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from ..controllers import relatorio_controller
from ..auth.auth import auth_handler
from ..resources.database import get_app_db_session
from ..auth.dependencies import is_udp, is_chefia, get_current_user
from ..providers.implementations.relatorio_provider import RelatorioProvider
from ..providers.interfaces.relatorio_provider_interface import RelatorioProviderInterface

# --- Router Definition ---

router = APIRouter(
    prefix="/api/relatorios",
    tags=["Relatórios"],
    dependencies=[Depends(auth_handler.decode_token)]
)

@router.get("/capacitacoes", response_model=List[Dict[str, Any]], dependencies=[Depends(is_udp)])
async def get_relatorio_capacitacoes(
    provider: RelatorioProviderInterface = Depends(RelatorioProvider) # Injeta a implementação do provider
):
    """
    Relatório completo de capacitações EAD.
    Requer perfil UDP.
    """
    return await relatorio_controller.gerar_relatorio_capacitacoes(provider)

@router.get("/udp/cursos-populares", response_model=List[Dict[str, Any]], dependencies=[Depends(is_udp)])
async def get_cursos_mais_inscritos_udp(
    db: AsyncSession = Depends(get_app_db_session),
    limit: int = 10
):
    """
    Relatório para a UDP: Lista os cursos mais inscritos/atribuídos.
    Requer perfil UDP.
    """
    return await relatorio_controller.listar_cursos_mais_inscritos_udp(db, limit)

# Placeholder para outros endpoints de relatório
@router.get("/udp/status-geral", response_model=List[Dict[str, Any]], dependencies=[Depends(is_udp)])
async def get_status_geral_udp(
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Relatório para a UDP: Status geral das capacitações.
    Requer perfil UDP.
    """
    return await relatorio_controller.get_relatorio_status_geral_udp(db)

@router.get("/udp/conformidade-lotacao", response_model=List[Dict[str, Any]], dependencies=[Depends(is_udp)])
async def get_conformidade_lotacao_udp(
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Relatório para a UDP: Conformidade por lotação.
    Requer perfil UDP.
    """
    return await relatorio_controller.get_relatorio_conformidade_lotacao_udp(db)

@router.get("/udp/certificados-pendentes", response_model=List[Dict[str, Any]], dependencies=[Depends(is_udp)])
async def get_certificados_pendentes_udp(
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Relatório para a UDP: Certificados pendentes de validação.
    Requer perfil UDP.
    """
    return await relatorio_controller.get_relatorio_certificados_pendentes_udp(db)

@router.get("/udp/usuarios-perfil-lotacao", response_model=List[Dict[str, Any]], dependencies=[Depends(is_udp)])
async def get_usuarios_perfil_lotacao_udp(
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Relatório para a UDP: Usuários por perfil e lotação.
    Requer perfil UDP.
    """
    return await relatorio_controller.get_relatorio_usuarios_por_perfil_lotacao_udp(db)

@router.get("/chefia/status-lotacao", response_model=List[Dict[str, Any]], dependencies=[Depends(is_chefia)])
async def get_status_lotacao_chefia(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Relatório para a Chefia: Status de cursos da minha lotação.
    Requer perfil Chefia.
    """
    lotacao = current_user.get("lotacao")
    if not lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")
    return await relatorio_controller.get_relatorio_status_lotacao_chefia(db, lotacao)

@router.get("/chefia/progresso-individual", response_model=List[Dict[str, Any]], dependencies=[Depends(is_chefia)])
async def get_progresso_individual_chefia(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Relatório para a Chefia: Progresso individual de subordinados.
    Requer perfil Chefia.
    """
    lotacao = current_user.get("lotacao")
    if not lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")
    return await relatorio_controller.get_relatorio_progresso_individual_chefia(db, lotacao)

@router.get("/chefia/certificados-pendentes", response_model=List[Dict[str, Any]], dependencies=[Depends(is_chefia)])
async def get_certificados_pendentes_chefia(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Relatório para a Chefia: Certificados pendentes de validação.
    Requer perfil Chefia.
    """
    lotacao = current_user.get("lotacao")
    if not lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")
    return await relatorio_controller.get_relatorio_certificados_pendentes_chefia(db, lotacao)
