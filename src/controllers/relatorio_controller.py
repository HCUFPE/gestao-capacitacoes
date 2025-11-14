from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Dict, Any

from ..models import Curso, Inscricao, Atribuicao, Usuario, StatusAtribuicao

async def listar_cursos_mais_inscritos_udp(db: AsyncSession, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Lista os cursos mais inscritos/atribuídos para a UDP.
    """
    stmt = (
        select(
            Curso.titulo,
            func.count(Inscricao.id).label("total_inscricoes"),
            func.count(Atribuicao.id).label("total_atribuicoes")
        )
        .outerjoin(Inscricao, Curso.id == Inscricao.curso_id)
        .outerjoin(Atribuicao, Curso.id == Atribuicao.curso_id)
        .group_by(Curso.id, Curso.titulo)
        .order_by(desc("total_inscricoes"), desc("total_atribuicoes"))
        .limit(limit)
    )
    result = await db.execute(stmt)
    return [
        {
            "titulo": r.titulo,
            "total_inscricoes": r.total_inscricoes,
            "total_atribuicoes": r.total_atribuicoes,
        }
        for r in result.all()
    ]

# Placeholder para outras funções de relatório
async def get_relatorio_status_geral_udp(db: AsyncSession) -> List[Dict[str, Any]]:
    """
    Placeholder para o relatório de status geral das capacitações para a UDP.
    """
    return []

async def get_relatorio_conformidade_lotacao_udp(db: AsyncSession) -> List[Dict[str, Any]]:
    """
    Placeholder para o relatório de conformidade por lotação para a UDP.
    """
    return []

async def get_relatorio_certificados_pendentes_udp(db: AsyncSession) -> List[Dict[str, Any]]:
    """
    Placeholder para o relatório de certificados pendentes de validação para a UDP.
    """
    return []

async def get_relatorio_usuarios_por_perfil_lotacao_udp(db: AsyncSession) -> List[Dict[str, Any]]:
    """
    Placeholder para o relatório de usuários por perfil e lotação para a UDP.
    """
    return []

async def get_relatorio_status_lotacao_chefia(db: AsyncSession, lotacao: str) -> List[Dict[str, Any]]:
    """
    Placeholder para o relatório de status de cursos da minha lotação para a Chefia.
    """
    return []

async def get_relatorio_progresso_individual_chefia(db: AsyncSession, lotacao: str) -> List[Dict[str, Any]]:
    """
    Placeholder para o relatório de progresso individual de subordinados para a Chefia.
    """
    return []

async def get_relatorio_certificados_pendentes_chefia(db: AsyncSession, lotacao: str) -> List[Dict[str, Any]]:
    """
    Placeholder para o relatório de certificados pendentes de validação para a Chefia.
    """
    return []
