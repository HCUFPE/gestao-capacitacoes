from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any
import logging

from ..models import Curso, Inscricao, Certificado, Usuario, Atribuicao, StatusAtribuicao

logger = logging.getLogger(__name__)

async def get_dashboard_stats(db: AsyncSession, user_id: str | None = None) -> Dict[str, Any]:
    """
    Calculates and returns key statistics for the dashboard (both global and personal).
    """
    try:
        # Total de Cursos
        total_cursos_stmt = select(func.count(Curso.id))
        total_cursos = (await db.execute(total_cursos_stmt)).scalar_one()

        # Total de Inscrições
        total_inscricoes_stmt = select(func.count(Inscricao.id))
        total_inscricoes = (await db.execute(total_inscricoes_stmt)).scalar_one()

        # Total de Certificados Validados
        total_certificados_stmt = select(func.count(Certificado.id)).where(Certificado.validado == True)
        total_certificados = (await db.execute(total_certificados_stmt)).scalar_one()

        # Total de Usuários
        total_usuarios_stmt = select(func.count(Usuario.id))
        total_usuarios = (await db.execute(total_usuarios_stmt)).scalar_one()

        minhas_inscricoes = 0
        meus_certificados_enviados = 0
        meus_certificados_validados = 0

        if user_id:
            minhas_inscricoes_stmt = select(func.count(Inscricao.id)).where(func.lower(Inscricao.user_id) == user_id.lower())
            minhas_inscricoes = (await db.execute(minhas_inscricoes_stmt)).scalar_one()

            meus_certificados_enviados_stmt = select(func.count(Atribuicao.id)).where(
                (func.lower(Atribuicao.user_id) == user_id.lower()) & (Atribuicao.certificado_id.isnot(None))
            )
            meus_certificados_enviados = (await db.execute(meus_certificados_enviados_stmt)).scalar_one()

            meus_certificados_validados_stmt = select(func.count(Atribuicao.id)).where(
                (func.lower(Atribuicao.user_id) == user_id.lower()) & (Atribuicao.status.in_([StatusAtribuicao.VALIDADO, StatusAtribuicao.CONCLUIDO]))
            )
            meus_certificados_validados = (await db.execute(meus_certificados_validados_stmt)).scalar_one()

        return {
            "total_cursos": total_cursos,
            "total_inscricoes": total_inscricoes,
            "total_certificados_validados": total_certificados,
            "total_usuarios": total_usuarios,
            "minhas_inscricoes": minhas_inscricoes,
            "meus_certificados_enviados": meus_certificados_enviados,
            "meus_certificados_validados": meus_certificados_validados,
        }
    except Exception as e:
        logger.error(f"Error calculating dashboard stats: {e}")
        # Return zeroed stats in case of an error to prevent frontend crashes
        return {
            "total_cursos": 0,
            "total_inscricoes": 0,
            "total_certificados_validados": 0,
            "total_usuarios": 0,
            "minhas_inscricoes": 0,
            "meus_certificados_enviados": 0,
            "meus_certificados_validados": 0,
        }
