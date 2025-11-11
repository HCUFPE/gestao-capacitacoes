from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List, Dict, Any
from uuid import uuid4

from ..models import Curso, Atribuicao

async def listar_cursos(db: AsyncSession) -> List[Curso]:
    """
    Lista todos os cursos usando o ORM do SQLAlchemy.
    """
    result = await db.execute(select(Curso))
    return result.scalars().all()

async def criar_curso(db: AsyncSession, curso_data: Dict[str, Any]) -> Curso:
    """
    Cria um novo curso usando o ORM do SQLAlchemy.
    """
    new_id = str(uuid4())
    curso_data["id"] = new_id
    
    new_curso = Curso(**curso_data)
    db.add(new_curso)
    await db.commit()
    await db.refresh(new_curso)
    return new_curso

async def atualizar_curso(db: AsyncSession, curso_id: str, curso_data: Dict[str, Any]) -> Curso | None:
    """
    Atualiza um curso existente usando o ORM do SQLAlchemy.
    """
    result = await db.execute(select(Curso).where(Curso.id == curso_id))
    curso = result.scalars().first()

    if curso:
        for key, value in curso_data.items():
            setattr(curso, key, value)
        await db.commit()
        await db.refresh(curso)
        return curso
    return None

async def deletar_curso(db: AsyncSession, curso_id: str) -> bool:
    """
    Deleta um curso e suas atribuições associadas usando o ORM do SQLAlchemy.
    """
    # Deletar atribuições relacionadas primeiro
    await db.execute(delete(Atribuicao).where(Atribuicao.curso_id == curso_id))
    
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

async def listar_cursos_recomendados_por_lotacao(db: AsyncSession, lotacao: str) -> List[Curso]:
    """
    Lista cursos recomendados para uma lotação específica.
    """
    print(f"DEBUG (Controller): lotacao received for comparison = {lotacao}")
    result = await db.execute(select(Curso).where(Curso.lotacao.ilike(lotacao)))
    return result.scalars().all()
