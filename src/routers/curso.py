from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..controllers import curso_controller
from ..auth.auth import auth_handler
from ..resources.database import get_app_db_session
from ..schemas.curso_schema import CursoCreate, CursoResponse, PaginatedCursoResponse
from ..models import Curso
from ..auth.dependencies import is_chefia, get_current_user, is_udp

# --- Router Definition ---

router = APIRouter(
    prefix="/api/cursos",
    tags=["Cursos"],
)

@router.get("", response_model=PaginatedCursoResponse, dependencies=[Depends(auth_handler.decode_token)])
@router.get("/", response_model=PaginatedCursoResponse, dependencies=[Depends(auth_handler.decode_token)])
async def listar_cursos(
    skip: int = 0,
    limit: int = 10,
    titulo: str | None = None,
    tema: str | None = None,
    db: AsyncSession = Depends(get_app_db_session)
):
    """Lista todos os cursos da fonte de dados interna com paginação e filtros."""
    return await curso_controller.listar_cursos(db, skip=skip, limit=limit, titulo=titulo, tema=tema)

@router.post("", response_model=CursoResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth_handler.decode_token), Depends(is_chefia)])
@router.post("/", response_model=CursoResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth_handler.decode_token), Depends(is_chefia)])
async def criar_curso(
    curso: CursoCreate,
    db: AsyncSession = Depends(get_app_db_session)
):
    """Cria um novo curso na fonte de dados interna. (Requer perfil de Chefia ou UDP)"""
    return await curso_controller.criar_curso(db, curso)

@router.put("/{curso_id}", response_model=CursoResponse, dependencies=[Depends(auth_handler.decode_token), Depends(is_chefia)])
async def atualizar_curso(
    curso_id: str,
    curso: CursoCreate,
    db: AsyncSession = Depends(get_app_db_session)
):
    """Atualiza um curso existente. (Requer perfil de Chefia ou UDP)"""
    updated_curso = await curso_controller.atualizar_curso(db, curso_id, curso)
    if updated_curso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    return updated_curso

@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth_handler.decode_token), Depends(is_chefia)])
async def deletar_curso(
    curso_id: str,
    db: AsyncSession = Depends(get_app_db_session)
):
    """Deleta um curso e suas atribuições. (Requer perfil de Chefia ou UDP)"""
    success = await curso_controller.deletar_curso(db, curso_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado.")
    return None

@router.post("/importar-csv", status_code=status.HTTP_200_OK, dependencies=[Depends(is_udp)])
async def importar_cursos_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Importa um catálogo de cursos a partir de um arquivo CSV (somente perfil UDP).
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Arquivo deve ser do tipo CSV.")
    
    file_bytes = await file.read()
    
    try:
        resultado = await curso_controller.importar_cursos_csv(file_bytes, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao processar arquivo: {str(e)}")
        
    if resultado.get("erros") and not resultado.get("novos") and not resultado.get("atualizados"):
        # Se só teve erro e não inseriu/atualizou nada (ex: erro de formato no inicio)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="\n".join(resultado["erros"]))
        
    return resultado

@router.get("/recommended", response_model=List[CursoResponse], dependencies=[Depends(auth_handler.decode_token)])
async def listar_cursos_recomendados(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Lista cursos recomendados para a lotação do usuário logado, excluindo os que ele já se inscreveu.
    """
    user_id = current_user.get("sub")
    
    # Fetch user's lotacao
    from ..models import Usuario
    from sqlalchemy.future import select
    user_stmt = select(Usuario.lotacao).where(Usuario.id == user_id)
    user_lotacao = (await db.execute(user_stmt)).scalar_one_or_none()

    if not user_lotacao:
        return []

    # Fetch enrolled course IDs
    from ..controllers import inscricao_controller # Local import to break circular dependency
    enrolled_inscricoes = await inscricao_controller.listar_inscricoes_por_usuario(db, user_id)
    enrolled_course_ids = [insc['curso_id'] for insc in enrolled_inscricoes]

    # Fetch assigned course IDs
    from ..controllers import atribuicao_controller # Local import to break circular dependency
    assigned_atribuicoes = await atribuicao_controller.listar_atribuicoes_por_usuario(db, user_id)
    assigned_course_ids = [atrib['curso_id'] for atrib in assigned_atribuicoes]

    # Combine both lists and remove duplicates
    excluded_course_ids = list(set(enrolled_course_ids + assigned_course_ids))

    return await curso_controller.listar_cursos_recomendados_por_lotacao(db, user_lotacao, excluded_course_ids)

@router.get("/genericos", response_model=List[CursoResponse], dependencies=[Depends(auth_handler.decode_token)])
async def listar_cursos_genericos(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Lista cursos genéricos (sem lotação específica), excluindo os que o usuário já se inscreveu ou que já foram atribuídos.
    """
    user_id = current_user.get("sub")
    
    # Fetch enrolled course IDs
    from ..controllers import inscricao_controller # Local import to break circular dependency
    enrolled_inscricoes = await inscricao_controller.listar_inscricoes_por_usuario(db, user_id)
    enrolled_course_ids = [insc['curso_id'] for insc in enrolled_inscricoes]

    # Fetch assigned course IDs
    from ..controllers import atribuicao_controller # Local import to break circular dependency
    assigned_atribuicoes = await atribuicao_controller.listar_atribuicoes_por_usuario(db, user_id)
    assigned_course_ids = [atrib['curso_id'] for atrib in assigned_atribuicoes]

    # Combine both lists and remove duplicates
    excluded_course_ids = list(set(enrolled_course_ids + assigned_course_ids))

    return await curso_controller.listar_cursos_genericos(db, excluded_course_ids)

@router.get("/{curso_id}", response_model=CursoResponse, dependencies=[Depends(auth_handler.decode_token)])
async def obter_curso(
    curso_id: str,
    db: AsyncSession = Depends(get_app_db_session)
):
    """Obtém um curso pelo ID a partir da fonte de dados interna."""
    curso = await curso_controller.obter_curso_por_id(db, curso_id)
    if curso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    return curso
