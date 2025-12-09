from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List, Dict, Any
from uuid import uuid4

from ..models import Curso, Atribuicao, Usuario, StatusAtribuicao
from ..schemas.curso_schema import CursoCreate
from datetime import datetime

from sqlalchemy import func

async def listar_cursos(db: AsyncSession, skip: int = 0, limit: int = 10, titulo: str = None, tema: str = None) -> Dict[str, Any]:
    """
    Lista cursos com paginação e filtros.
    """
    stmt = select(Curso)
    
    if titulo:
        stmt = stmt.where(Curso.titulo.ilike(f"%{titulo}%"))
    if tema:
        stmt = stmt.where(Curso.tema.ilike(f"%{tema}%"))
    
    # Get total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = await db.scalar(count_stmt)

    # Apply pagination
    stmt = stmt.offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    items = result.scalars().all()
    
    return {"items": items, "total": total}

async def criar_curso(db: AsyncSession, curso_data: CursoCreate) -> Curso:
    """
    Cria um novo curso e, opcionalmente, o atribui a todos os usuários de um setor.
    """
    new_id = str(uuid4())
    
    # Create the course
    new_curso = Curso(
        id=new_id,
        titulo=curso_data.titulo,
        certificadora=curso_data.certificadora,
        carga_horaria=curso_data.carga_horaria,
        link=curso_data.link,
        tema=curso_data.tema,
        ano_gd=curso_data.ano_gd,
        lotacao_id=curso_data.lotacao_id,
        atribuir_a_todos=curso_data.atribuir_a_todos,
        conteudista=curso_data.conteudista,
        disponibilidade_dias=curso_data.disponibilidade_dias,
        tipo_oferta=curso_data.tipo_oferta,
        apresentacao=curso_data.apresentacao,
        publico_alvo=curso_data.publico_alvo,
        conteudo_programatico=curso_data.conteudo_programatico,
        data_lancamento=curso_data.data_lancamento,
        acessibilidade=curso_data.acessibilidade,
        observacao=curso_data.observacao
    )
    db.add(new_curso)
    
    # If the flag is set, assign the course to all users in the lotacao
    if curso_data.atribuir_a_todos and curso_data.lotacao_id:
        # 1. Find all users in the specified lotacao
        user_stmt = select(Usuario).where(Usuario.lotacao.ilike(curso_data.lotacao_id))
        users_to_assign = (await db.execute(user_stmt)).scalars().all()
        
        # 2. Create an Atribuicao for each user
        for user in users_to_assign:
            new_atribuicao = Atribuicao(
                id=str(uuid4()),
                user_id=user.id,
                curso_id=new_id,
                status=StatusAtribuicao.PENDENTE,
                atribuido_em=datetime.utcnow()
            )
            db.add(new_atribuicao)

    await db.commit()
    await db.refresh(new_curso)
    return new_curso

async def atualizar_curso(db: AsyncSession, curso_id: str, curso_data: CursoCreate) -> Curso | None:
    """
    Atualiza um curso existente e, opcionalmente, o atribui a todos os usuários de um setor
    que ainda não o possuem.
    """
    result = await db.execute(select(Curso).where(Curso.id == curso_id))
    curso = result.scalars().first()

    if not curso:
        return None

    curso.atribuir_a_todos = curso_data.atribuir_a_todos
    # Update course fields
    for key, value in curso_data.dict(exclude_unset=True).items():
        if hasattr(curso, key):
            setattr(curso, key, value)

    # If the flag is set, assign the course to users in the lotacao who don't have it yet
    if curso_data.atribuir_a_todos and curso_data.lotacao_id and curso_data.lotacao_id != '':
        # 1. Find all users in the specified lotacao
        user_stmt = select(Usuario).where(Usuario.lotacao.ilike(curso_data.lotacao_id))
        users_in_lotacao = (await db.execute(user_stmt)).scalars().all()
        
        # 2. Find all users who already have an assignment for this course
        existing_atribuicoes_stmt = select(Atribuicao.user_id).where(Atribuicao.curso_id == curso_id)
        existing_assigned_users = (await db.execute(existing_atribuicoes_stmt)).scalars().all()
        existing_user_ids = set(existing_assigned_users)

        # 3. Create an Atribuicao for each user who doesn't have one
        for user in users_in_lotacao:
            if user.id not in existing_user_ids:
                new_atribuicao = Atribuicao(
                    id=str(uuid4()),
                    user_id=user.id,
                    curso_id=curso_id,
                    status=StatusAtribuicao.PENDENTE,
                    atribuido_em=datetime.utcnow()
                )
                db.add(new_atribuicao)
    elif not curso_data.atribuir_a_todos and curso_data.lotacao_id and curso_data.lotacao_id != '': # Only delete if lotacao_id is present
        # If the flag is unchecked, remove all 'Pendente' assignments for this course
        stmt_delete = delete(Atribuicao).where(
            Atribuicao.curso_id == curso_id,
            Atribuicao.status == StatusAtribuicao.PENDENTE
        )
        await db.execute(stmt_delete)
        
    await db.commit()
    await db.refresh(curso)
    return curso

async def deletar_curso(db: AsyncSession, curso_id: str) -> bool:
    """
    Deleta um curso e suas atribuições, inscrições e certificados associados.
    """
    # Deletar atribuições relacionadas
    await db.execute(delete(Atribuicao).where(Atribuicao.curso_id == curso_id))
    
    # Deletar inscrições relacionadas
    from ..models import Inscricao # Import local para evitar circular dependency
    await db.execute(delete(Inscricao).where(Inscricao.curso_id == curso_id))

    # Deletar certificados relacionados
    from ..models import Certificado # Import local para evitar circular dependency
    await db.execute(delete(Certificado).where(Certificado.curso_id == curso_id))
    
    # Deletar o curso
    result = await db.execute(select(Curso).where(Curso.id == curso_id))
    curso = result.scalars().first()
    if curso:
        await db.delete(curso)
        await db.commit()
        return True
    return False

async def obter_curso_por_id(db: AsyncSession, curso_id: str) -> Curso | None:
    """
    Obtém um curso pelo ID usando o ORM do SQLAlchemy.
    """
    result = await db.execute(select(Curso).where(Curso.id == curso_id))
    return result.scalars().first()

async def listar_cursos_recomendados_por_lotacao(db: AsyncSession, lotacao: str, excluded_course_ids: List[str]) -> List[Curso]:
    """
    Lista cursos recomendados para uma lotação específica, excluindo os que o usuário já se inscreveu ou que já foram atribuídos.
    """
    stmt = select(Curso).where(
        Curso.lotacao_id.ilike(lotacao),
        Curso.atribuir_a_todos == False # Exclui cursos que são atribuídos a todos
    )
    if excluded_course_ids:
        stmt = stmt.where(Curso.id.notin_(excluded_course_ids))
    
    result = await db.execute(stmt)
    return result.scalars().all()

async def listar_cursos_genericos(db: AsyncSession, excluded_course_ids: List[str]) -> List[Curso]:
    """
    Lista cursos genéricos (sem lotação específica), excluindo os que o usuário já se inscreveu ou que já foram atribuídos.
    """
    stmt = select(Curso).where(
        (Curso.lotacao_id.is_(None)) | (Curso.lotacao_id == '')
    )
    if excluded_course_ids:
        stmt = stmt.where(Curso.id.notin_(excluded_course_ids))
    
    result = await db.execute(stmt)
    return result.scalars().all()
