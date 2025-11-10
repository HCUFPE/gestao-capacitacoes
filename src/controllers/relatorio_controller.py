from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..models import Curso, Atribuicao, StatusAtribuicao, Usuario

async def relatorio_cursos_por_lotacao(db: AsyncSession, lotacao: str) -> List[Dict[str, Any]]:
    """
    Gera um relatório de cursos e seu status de conclusão para uma dada lotação.
    """
    # Subquery para contar atribuições concluídas (Validadas) por curso
    subquery_concluidos = (
        select(
            Atribuicao.curso_id,
            func.count(Atribuicao.id).label("concluidos")
        )
        .join(Usuario, Atribuicao.user_id == Usuario.id)
        .where(
            Usuario.lotacao == lotacao,
            Atribuicao.status == StatusAtribuicao.VALIDADO
        )
        .group_by(Atribuicao.curso_id)
        .subquery()
    )

    # Subquery para contar total de atribuições por curso
    subquery_total = (
        select(
            Atribuicao.curso_id,
            func.count(Atribuicao.id).label("total")
        )
        .join(Usuario, Atribuicao.user_id == Usuario.id)
        .where(Usuario.lotacao == lotacao)
        .group_by(Atribuicao.curso_id)
        .subquery()
    )

    # Query principal
    query = (
        select(
            Curso.titulo,
            Curso.ano_gd,
            func.coalesce(subquery_total.c.total, 0).label("total_atribuicoes"),
            func.coalesce(subquery_concluidos.c.concluidos, 0).label("total_concluidos")
        )
        .join_from(Curso, subquery_total, Curso.id == subquery_total.c.curso_id, isouter=True)
        .join_from(Curso, subquery_concluidos, Curso.id == subquery_concluidos.c.curso_id, isouter=True)
        .where(Curso.lotacao == lotacao)
    )

    result = await db.execute(query)
    return [dict(row) for row in result.mappings()]