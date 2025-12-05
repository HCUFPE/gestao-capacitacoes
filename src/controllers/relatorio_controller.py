from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Dict, Any

from ..models import Curso, Inscricao, Atribuicao, Usuario, StatusAtribuicao
from ..providers.implementations.relatorio_provider import RelatorioProvider
from ..providers.interfaces.relatorio_provider_interface import RelatorioProviderInterface

async def gerar_relatorio_capacitacoes(provider: RelatorioProviderInterface) -> List[Dict[str, Any]]:
    """
    Gera o relatório completo de capacitações EAD, consolidando dados de usuários, cursos e certificados.
    """
    return await provider.listar_dados_capacitacoes()

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
    Gera um relatório com a contagem de atribuições para cada status.
    """
    stmt = (
        select(
            Atribuicao.status,
            func.count(Atribuicao.id).label("total")
        )
        .group_by(Atribuicao.status)
    )
    result = await db.execute(stmt)
    
    # Inicializa um dicionário com todos os status para garantir que todos apareçam no resultado
    status_counts = {status.value: 0 for status in StatusAtribuicao}
    
    for row in result.all():
        status_counts[row.status] = row.total
        
    # Converte o dicionário para o formato de lista de dicionários esperado
    return [{"name": status, "value": count} for status, count in status_counts.items()]

async def get_relatorio_conformidade_lotacao_udp(db: AsyncSession) -> List[Dict[str, Any]]:
    """
    Gera um relatório de conformidade por lotação, contando as atribuições por status.
    """
    stmt = (
        select(
            Usuario.lotacao,
            Atribuicao.status,
            func.count(Atribuicao.id).label("total")
        )
        .join(Usuario, Atribuicao.user_id == Usuario.id)
        .group_by(Usuario.lotacao, Atribuicao.status)
        .order_by(Usuario.lotacao, Atribuicao.status)
    )
    result = await db.execute(stmt)
    
    conformidade_por_lotacao: Dict[str, Dict[str, Any]] = {}
    
    for row in result.all():
        lotacao = row.lotacao
        status = row.status
        total = row.total
        
        if lotacao not in conformidade_por_lotacao:
            conformidade_por_lotacao[lotacao] = {
                "lotacao": lotacao,
                "Pendente": 0,
                "Em Andamento": 0,
                "Realizado": 0,
                "Validado": 0,
                "Recusado": 0,
                "Total Atribuições": 0,
            }
        
        conformidade_por_lotacao[lotacao][status] = total
        conformidade_por_lotacao[lotacao]["Total Atribuições"] += total
            
    return list(conformidade_por_lotacao.values())

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
