from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from uuid import uuid4

from ..models import Curso, AnoGD, Atribuicao
from . import atribuicao_controller # Import the atribuicao_controller

async def listar_cursos(db: AsyncSession) -> List[Curso]:
    """
    Lista todos os cursos usando o ORM do SQLAlchemy.
    """
    result = await db.execute(select(Curso))
    return result.scalars().all()

async def criar_curso(db: AsyncSession, curso_data: Dict[str, Any]) -> Curso:
    """
    Cria um novo curso e automaticamente atribui a todos os usuários da lotação.
    """
    new_id = str(uuid4())
    curso_data["id"] = new_id
    
    # Converte o ano para o enum, se necessário
    if "ano_gd" in curso_data and isinstance(curso_data["ano_gd"], int):
        curso_data["ano_gd"] = AnoGD(curso_data["ano_gd"])

    new_curso = Curso(**curso_data)
    db.add(new_curso)
    await db.commit()
    await db.refresh(new_curso)

    # Passo 2: Chamar a função para criar as atribuições
    await atribuicao_controller.criar_atribuicoes_para_lotacao(
        db=db,
        curso_id=new_curso.id,
        lotacao=new_curso.lotacao
    )

    return new_curso

async def obter_curso_por_id(db: AsyncSession, curso_id: str) -> Curso | None:
    """
    Obtém um curso pelo ID usando o ORM do SQLAlchemy.
    """
    result = await db.execute(select(Curso).where(Curso.id == curso_id))
    return result.scalars().first()

async def atualizar_curso(db: AsyncSession, curso_id: str, curso_data: Dict[str, Any]) -> Curso | None:
    """
    Atualiza um curso existente.
    """
    # Converte o ano para o enum, se necessário
    if "ano_gd" in curso_data and isinstance(curso_data["ano_gd"], int):
        curso_data["ano_gd"] = AnoGD(curso_data["ano_gd"])
        
    stmt = (
        update(Curso)
        .where(Curso.id == curso_id)
        .values(**curso_data)
        .returning(Curso)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()

async def deletar_curso(db: AsyncSession, curso_id: str) -> bool:
    """
    Deleta um curso e todas as suas atribuições associadas.
    Retorna True se a deleção foi bem-sucedida, False caso contrário.
    """
    # Primeiro, deleta as atribuições associadas
    stmt_delete_atribuicoes = delete(Atribuicao).where(Atribuicao.curso_id == curso_id)
    await db.execute(stmt_delete_atribuicoes)
    
    # Depois, deleta o curso
    stmt_delete_curso = delete(Curso).where(Curso.id == curso_id)
    result = await db.execute(stmt_delete_curso)
    
    await db.commit()
    # rowcount > 0 significa que o curso foi encontrado e deletado
    return result.rowcount > 0
