from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from ..controllers import relatorio_controller, usuario_controller
from ..auth.auth import auth_handler
from ..resources.database import get_app_db_session
from ..auth.dependencies import is_udp, is_chefia, get_current_user
from ..models import PerfilUsuario
from ..providers.implementations.relatorio_provider import RelatorioProvider
from ..providers.interfaces.relatorio_provider_interface import RelatorioProviderInterface
from ..models import Usuario
from ..helpers import excel_helper
from sqlalchemy import select as sa_select

# --- Dependency Factory ---
def get_relatorio_provider(db: AsyncSession = Depends(get_app_db_session)) -> RelatorioProviderInterface:
    return RelatorioProvider(db)

# --- Router Definition ---

router = APIRouter(
    prefix="/api/relatorios",
    tags=["Relatórios"],
    dependencies=[Depends(auth_handler.decode_token)]
)


def is_chefia_or_udp(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency that checks if the current user has 'Chefia' or 'UDP' profile.
    """
    perfil = current_user.get("perfil")
    if perfil not in [PerfilUsuario.CHEFIA.value, PerfilUsuario.UDP.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Requer perfil de Chefia ou UDP."
        )
    return current_user

@router.get("/capacitacoes", response_model=List[Dict[str, Any]], dependencies=[Depends(is_udp)])
async def get_relatorio_capacitacoes(
    ano: str | None = None,
    vinculo: str | None = None,
    provider: RelatorioProviderInterface = Depends(get_relatorio_provider)
):
    """
    Relatório completo de capacitações EAD.
    Requer perfil UDP.
    Suporta filtros opcionais por ano e vínculo.
    """
    return await relatorio_controller.gerar_relatorio_capacitacoes(provider, ano=ano, vinculo=vinculo)

@router.get("/capacitacoes/export/excel", dependencies=[Depends(is_udp)])
async def export_relatorio_excel(
    ano: str | None = None,
    vinculo: str | None = None,
    provider: RelatorioProviderInterface = Depends(get_relatorio_provider)
):
    """
    Exporta o relatório de capacitações para Excel.
    Suporta filtros opcionais por ano e vínculo.
    """
    file_stream = await relatorio_controller.exportar_relatorio_excel(provider, ano=ano, vinculo=vinculo)
    headers = {
        'Content-Disposition': 'attachment; filename="relatorio_capacitacoes.xlsx"'
    }
    return StreamingResponse(file_stream, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

@router.get("/capacitacoes/export/pdf", dependencies=[Depends(is_udp)])
async def export_relatorio_pdf(
    ano: str | None = None,
    vinculo: str | None = None,
    provider: RelatorioProviderInterface = Depends(get_relatorio_provider)
):
    """
    Exporta o relatório de capacitações para PDF.
    Suporta filtros opcionais por ano e vínculo.
    """
    file_stream = await relatorio_controller.exportar_relatorio_pdf(provider, ano=ano, vinculo=vinculo)
    headers = {
        'Content-Disposition': 'attachment; filename="relatorio_capacitacoes.pdf"'
    }
    return StreamingResponse(file_stream, media_type='application/pdf', headers=headers)

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
    ano: str | None = None,
    vinculo: str | None = None,
    current_user: dict = Depends(get_current_user),
    provider: RelatorioProviderInterface = Depends(get_relatorio_provider),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Relatório para a Chefia: Status de cursos da minha lotação.
    Requer perfil Chefia.
    Suporta filtros opcionais por ano e vínculo.
    """
    user_id = current_user.get("sub")
    user = await usuario_controller.get_user_by_username(db, user_id)
    
    if not user or not user.lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")
        
    return await relatorio_controller.get_relatorio_status_lotacao_chefia(provider, user.lotacao, ano=ano, vinculo=vinculo)

@router.get("/chefia/progresso-individual", response_model=List[Dict[str, Any]], dependencies=[Depends(is_chefia)])
async def get_progresso_individual_chefia(
    ano: str | None = None,
    vinculo: str | None = None,
    current_user: dict = Depends(get_current_user),
    provider: RelatorioProviderInterface = Depends(get_relatorio_provider),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Relatório para a Chefia: Progresso individual de subordinados.
    Requer perfil Chefia.
    Suporta filtros opcionais por ano e vínculo.
    """
    user_id = current_user.get("sub")
    user = await usuario_controller.get_user_by_username(db, user_id)
    
    if not user or not user.lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")
        
    return await relatorio_controller.get_relatorio_progresso_individual_chefia(provider, user.lotacao, ano=ano, vinculo=vinculo)

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


@router.get("/chefia/subordinado/{subordinado_id}", response_model=List[Dict[str, Any]], dependencies=[Depends(is_chefia)])
async def get_subordinado_detalhes(
    subordinado_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Retorna os detalhes de um subordinado específico: cursos, status, certificados.
    Chefia só pode acessar subordinados da própria lotação.
    """
    user_id = current_user.get("sub")
    user = await usuario_controller.get_user_by_username(db, user_id)

    if not user or not user.lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")

    from ..models import Atribuicao, Certificado, Curso
    from sqlalchemy.orm import selectinload

    # Verificar se o subordinado pertence à mesma lotação
    sub_stmt = sa_select(Usuario.id, Usuario.nome, Usuario.lotacao).where(Usuario.id == subordinado_id)
    sub_result = await db.execute(sub_stmt)
    sub_row = sub_result.mappings().first()

    if not sub_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subordinado não encontrado.")

    if sub_row["lotacao"] != user.lotacao:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você só pode acessar subordinados da sua lotação.")

    # Buscar atribuições com detalhes do curso e certificado
    atrib_stmt = (
        sa_select(Atribuicao, Curso, Certificado)
        .options(selectinload(Atribuicao.curso), selectinload(Atribuicao.certificado))
        .join(Curso, Atribuicao.curso_id == Curso.id)
        .outerjoin(Certificado, Atribuicao.certificado_id == Certificado.id)
        .where(Atribuicao.user_id == subordinado_id)
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


@router.get("/vinculos", response_model=List[str], dependencies=[Depends(auth_handler.decode_token)])
async def get_vinculos_disponiveis(
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Lista todos os vínculos únicos disponíveis no sistema.
    """
    stmt = sa_select(Usuario.vinculo).where(Usuario.vinculo.isnot(None)).distinct().order_by(Usuario.vinculo)
    result = await db.execute(stmt)
    return [row[0] for row in result.all()]


@router.get("/usuario/{user_id}/detalhes", response_model=List[Dict[str, Any]], dependencies=[Depends(is_chefia_or_udp)])
async def get_usuario_detalhes(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Retorna os detalhes de um usuário: cursos, status, certificados.
    Chefia só pode acessar usuários da mesma lotação; UDP pode acessar qualquer usuário.
    """
    await relatorio_controller.can_access_user_details(db, current_user, user_id)
    return await relatorio_controller.get_usuario_detalhes(db, user_id)


@router.get("/chefia/consolidado", response_model=List[Dict[str, Any]], dependencies=[Depends(is_chefia)])
async def get_consolidado_chefia(
    ano: str | None = None,
    vinculo: str | None = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Relatório consolidado para a Chefia.
    Filtra por lotação da chefia + filtros opcionais por ano e vínculo.
    """
    user_id = current_user.get("sub")
    user = await usuario_controller.get_user_by_username(db, user_id)

    if not user or not user.lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")

    return await relatorio_controller.get_relatorio_consolidado(
        db, lotacao=user.lotacao, ano=ano, vinculo=vinculo
    )


@router.get("/udp/consolidado", response_model=List[Dict[str, Any]], dependencies=[Depends(is_udp)])
async def get_consolidado_udp(
    ano: str | None = None,
    vinculo: str | None = None,
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Relatório consolidado para a UDP (todas as lotações).
    Suporta filtros opcionais por ano e vínculo.
    """
    return await relatorio_controller.get_relatorio_consolidado(
        db, lotacao=None, ano=ano, vinculo=vinculo
    )


@router.get("/chefia/consolidado/export/excel", dependencies=[Depends(is_chefia)])
async def export_consolidado_excel_chefia(
    ano: str | None = None,
    vinculo: str | None = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Exporta o relatório consolidado para Excel (Chefia).
    """
    user_id = current_user.get("sub")
    user = await usuario_controller.get_user_by_username(db, user_id)

    if not user or not user.lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")

    data = await relatorio_controller.get_relatorio_consolidado(
        db, lotacao=user.lotacao, ano=ano, vinculo=vinculo
    )
    file_stream = await excel_helper.export_to_excel(data)
    headers = {'Content-Disposition': 'attachment; filename="relatorio_consolidado.xlsx"'}
    return StreamingResponse(file_stream, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)


@router.get("/chefia/consolidado/export/pdf", dependencies=[Depends(is_chefia)])
async def export_consolidado_pdf_chefia(
    ano: str | None = None,
    vinculo: str | None = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Exporta o relatório consolidado para PDF (Chefia).
    """
    user_id = current_user.get("sub")
    user = await usuario_controller.get_user_by_username(db, user_id)

    if not user or not user.lotacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lotação do usuário não encontrada.")

    data = await relatorio_controller.get_relatorio_consolidado(
        db, lotacao=user.lotacao, ano=ano, vinculo=vinculo
    )
    file_stream = await relatorio_controller.export_consolidado_to_pdf(data)
    headers = {'Content-Disposition': 'attachment; filename="relatorio_consolidado.pdf"'}
    return StreamingResponse(file_stream, media_type='application/pdf', headers=headers)


@router.get("/udp/consolidado/export/excel", dependencies=[Depends(is_udp)])
async def export_consolidado_excel_udp(
    ano: str | None = None,
    vinculo: str | None = None,
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Exporta o relatório consolidado para Excel (UDP).
    """
    data = await relatorio_controller.get_relatorio_consolidado(
        db, lotacao=None, ano=ano, vinculo=vinculo
    )
    file_stream = await excel_helper.export_to_excel(data)
    headers = {'Content-Disposition': 'attachment; filename="relatorio_consolidado.xlsx"'}
    return StreamingResponse(file_stream, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)


@router.get("/udp/consolidado/export/pdf", dependencies=[Depends(is_udp)])
async def export_consolidado_pdf_udp(
    ano: str | None = None,
    vinculo: str | None = None,
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Exporta o relatório consolidado para PDF (UDP).
    """
    data = await relatorio_controller.get_relatorio_consolidado(
        db, lotacao=None, ano=ano, vinculo=vinculo
    )
    file_stream = await relatorio_controller.export_consolidado_to_pdf(data)
    headers = {'Content-Disposition': 'attachment; filename="relatorio_consolidado.pdf"'}
    return StreamingResponse(file_stream, media_type='application/pdf', headers=headers)
