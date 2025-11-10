from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from ..controllers import relatorio_controller
from ..auth.auth import auth_handler
from ..resources.database import get_app_db_session
from ..helpers import excel_helper, pdf_helper

router = APIRouter(
    prefix="/api/relatorios",
    tags=["Relatórios"],
)

@router.get("/cursos-por-lotacao", dependencies=[Depends(auth_handler.decode_token)])
async def get_relatorio_cursos_por_lotacao(
    lotacao: str,
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Gera um relatório de status de conclusão de cursos para uma lotação específica.
    """
    data = await relatorio_controller.relatorio_cursos_por_lotacao(db, lotacao)
    return data

@router.get("/exportar-excel", dependencies=[Depends(auth_handler.decode_token)])
async def exportar_relatorio_excel(
    lotacao: str,
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Exporta o relatório de cursos por lotação para um arquivo Excel.
    """
    data = await relatorio_controller.relatorio_cursos_por_lotacao(db, lotacao)
    
    # Converte os dados para um formato simples se necessário
    data_to_export = [
        {
            "Curso": item["titulo"],
            "Ano GD": item["ano_gd"].value if item["ano_gd"] else None,
            "Total de Atribuições": item["total_atribuicoes"],
            "Total de Concluídos": item["total_concluidos"],
        }
        for item in data
    ]

    excel_file = await excel_helper.export_to_excel(data_to_export)
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=relatorio_{lotacao}.xlsx"}
    )

@router.get("/exportar-pdf", dependencies=[Depends(auth_handler.decode_token)])
async def exportar_relatorio_pdf(
    lotacao: str,
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Exporta o relatório de cursos por lotação para um arquivo PDF.
    """
    data = await relatorio_controller.relatorio_cursos_por_lotacao(db, lotacao)
    
    data_to_export = [
        {
            "Curso": item["titulo"],
            "Ano GD": str(item["ano_gd"].value) if item["ano_gd"] else "N/A",
            "Atribuições": str(item["total_atribuicoes"]),
            "Concluídos": str(item["total_concluidos"]),
        }
        for item in data
    ]

    pdf_file = await pdf_helper.export_to_pdf(data_to_export, filename=f"relatorio_{lotacao}.pdf")
    
    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=relatorio_{lotacao}.pdf"}
    )