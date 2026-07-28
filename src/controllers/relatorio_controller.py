from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Dict, Any
from io import BytesIO

from ..models import Curso, Inscricao, Atribuicao, Usuario, StatusAtribuicao, PerfilUsuario, Certificado
from ..providers.implementations.relatorio_provider import RelatorioProvider
from ..providers.interfaces.relatorio_provider_interface import RelatorioProviderInterface
from ..helpers import excel_helper, pdf_helper

async def gerar_relatorio_capacitacoes(
    provider: RelatorioProviderInterface,
    ano: str | None = None,
    vinculo: str | None = None
) -> List[Dict[str, Any]]:
    """
    Gera o relatório completo de capacitações EAD, consolidando dados de usuários, cursos e certificados.
    Suporta filtros opcionais por ano e vínculo.
    """
    return await provider.listar_dados_capacitacoes(ano=ano, vinculo=vinculo)

async def exportar_relatorio_excel(
    provider: RelatorioProviderInterface,
    ano: str | None = None,
    vinculo: str | None = None
) -> BytesIO:
    """
    Gera o arquivo Excel do relatório de capacitações.
    Suporta filtros opcionais por ano e vínculo.
    """
    data = await provider.listar_dados_capacitacoes(ano=ano, vinculo=vinculo)
    return await excel_helper.export_to_excel(data)

async def export_consolidado_to_pdf(data: List[Dict[str, Any]], filename: str = "relatorio_consolidado.pdf") -> BytesIO:
    """
    Gera PDF do relatório consolidado.
    """
    return await pdf_helper.export_to_pdf(data, filename=filename)


async def exportar_relatorio_pdf(
    provider: RelatorioProviderInterface,
    ano: str | None = None,
    vinculo: str | None = None
) -> BytesIO:
    """
    Gera o arquivo PDF do relatório de capacitações.
    Suporta filtros opcionais por ano e vínculo.
    """
    data = await provider.listar_dados_capacitacoes(ano=ano, vinculo=vinculo)
    return await pdf_helper.export_to_pdf(data, filename="relatorio_capacitacoes.pdf")

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

async def get_relatorio_status_lotacao_chefia(
    provider: RelatorioProviderInterface,
    lotacao: str,
    ano: str | None = None,
    vinculo: str | None = None
) -> List[Dict[str, Any]]:
    """
    Relatório para a Chefia: Status de cursos da minha lotação.
    Suporta filtros opcionais por ano e vínculo.
    """
    return await provider.get_status_lotacao(lotacao, ano=ano, vinculo=vinculo)

async def get_relatorio_progresso_individual_chefia(
    provider: RelatorioProviderInterface,
    lotacao: str,
    ano: str | None = None,
    vinculo: str | None = None
) -> List[Dict[str, Any]]:
    """
    Relatório para a Chefia: Progresso individual de subordinados.
    Suporta filtros opcionais por ano e vínculo.
    """
    return await provider.get_progresso_equipe(lotacao, ano=ano, vinculo=vinculo)

async def get_relatorio_certificados_pendentes_chefia(db: AsyncSession, lotacao: str) -> List[Dict[str, Any]]:
    """
    Placeholder para o relatório de certificados pendentes de validação para a Chefia.
    """
    return []


async def get_usuario_detalhes(
    db: AsyncSession,
    user_id: str
) -> List[Dict[str, Any]]:
    """
    Retorna os detalhes de um usuário: cursos, status, certificados.
    Reutiliza a lógica do endpoint de subordinado da Chefia.
    """
    from sqlalchemy.orm import selectinload

    atrib_stmt = (
        select(Atribuicao, Curso, Certificado)
        .options(selectinload(Atribuicao.curso), selectinload(Atribuicao.certificado))
        .join(Curso, Atribuicao.curso_id == Curso.id)
        .outerjoin(Certificado, Atribuicao.certificado_id == Certificado.id)
        .where(Atribuicao.user_id == user_id)
    )
    atrib_result = await db.execute(atrib_stmt)
    atrib_rows = atrib_result.all()

    return [
        {
            "id": a.id,
            "user_id": a.user_id,
            "curso_id": a.curso_id,
            "status": a.status.value if hasattr(a.status, 'value') else str(a.status),
            "atribuido_em": a.atribuido_em.isoformat() if a.atribuido_em else None,
            "certificado_id": c.id if c else None,
            "certificado_file_path": c.file_path if c else None,
            "certificado_link": c.link if c else None,
            "curso": {
                "id": curso.id,
                "titulo": curso.titulo,
                "certificadora": curso.certificadora,
                "carga_horaria": curso.carga_horaria,
                "ano_gd": curso.ano_gd,
                "link": curso.link,
            },
        }
        for a, curso, c in atrib_rows
    ]


async def can_access_user_details(
    db: AsyncSession,
    current_user: dict,
    target_user_id: str
) -> None:
    """
    Valida se o usuário autenticado pode acessar os detalhes de outro usuário.
    - UDP: pode acessar qualquer usuário
    - Chefia: só pode acessar usuários da mesma lotação
    - Trabalhador: não pode acessar
    
    Raises HTTPException 403 or 404 on failure.
    """
    from fastapi import HTTPException, status

    perfil = current_user.get("perfil")
    
    # Trabalhador não tem acesso
    if perfil == PerfilUsuario.TRABALHADOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Perfil não autorizado."
        )

    # Verificar se o usuário alvo existe
    stmt = select(Usuario.id, Usuario.nome, Usuario.lotacao).where(Usuario.id == target_user_id)
    result = await db.execute(stmt)
    target = result.mappings().first()

    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    # Chefia só pode acessar usuários da mesma lotação
    if perfil == PerfilUsuario.CHEFIA.value:
        current_user_id = current_user.get("sub")
        current_user_stmt = select(Usuario.lotacao).where(Usuario.id == current_user_id)
        current_result = await db.execute(current_user_stmt)
        current_user_row = current_result.mappings().first()

        if not current_user_row or not current_user_row["lotacao"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lotação do usuário não encontrada."
            )

        if target["lotacao"] != current_user_row["lotacao"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você só pode acessar usuários da sua lotação."
            )
    # UDP (perfil == "UDP") pode acessar qualquer usuário - sem restrição extra


async def get_relatorio_consolidado(
    db: AsyncSession,
    lotacao: str | None = None,
    ano: str | None = None,
    vinculo: str | None = None
) -> List[Dict[str, Any]]:
    """
    Relatório consolidado: nome, curso, status, data_envio_certificado, vinculo, certificado_enviado.
    Se lotacao for fornecido, filtra por chefia. Caso contrário (UDP), retorna tudo.
    """
    stmt = (
        select(
            Usuario.id,
            Usuario.nome,
            Usuario.vinculo,
            Usuario.lotacao.label("setor"),
            Curso.titulo.label("nome_curso"),
            Curso.certificadora,
            Curso.carga_horaria,
            Curso.ano_gd,
            Atribuicao.status,
            Atribuicao.data_conclusao,
            Certificado.file_path.label("certificado_file_path"),
            Certificado.link.label("certificado_link"),
            Certificado.id.label("certificado_id"),
        )
        .join(Usuario, Atribuicao.user_id == Usuario.id)
        .join(Curso, Atribuicao.curso_id == Curso.id)
        .outerjoin(Certificado, Atribuicao.certificado_id == Certificado.id)
    )

    if lotacao:
        stmt = stmt.where(Usuario.lotacao == lotacao)

    if vinculo:
        stmt = stmt.where(Usuario.vinculo == vinculo)

    if ano:
        stmt = stmt.where(Curso.ano_gd == str(ano))

    stmt = stmt.order_by(Usuario.nome, Curso.titulo)
    result = await db.execute(stmt)

    rows = result.mappings().all()
    data = []
    for row in rows:
        data.append({
            "id": row["id"],
            "nome": row["nome"],
            "vinculo": row["vinculo"] or "Não informado",
            "setor": row["setor"],
            "nome_curso": row["nome_curso"],
            "certificadora": row["certificadora"],
            "carga_horaria": row["carga_horaria"],
            "ano_gd": row["ano_gd"],
            "status": row["status"],
            "data_envio_certificado": row["data_conclusao"].isoformat() if row["data_conclusao"] else None,
            "vinculo_display": row["vinculo"] or "Não informado",
            "certificado_enviado": "Sim" if row["certificado_id"] else "Não",
            "certificado_id": row["certificado_id"],
            "certificado_file_path": row["certificado_file_path"],
            "certificado_link": row["certificado_link"],
        })

    return data
