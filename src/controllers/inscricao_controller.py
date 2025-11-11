from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert
from sqlalchemy.orm import selectinload
from uuid import uuid4

from ..models import Inscricao, Curso, Usuario

async def inscrever_usuario_em_curso(db: AsyncSession, usuario_id: str, curso_id: str) -> Inscricao:
    """
    Inscreve um usuário em um curso.
    """
    new_inscricao = Inscricao(
        id=str(uuid4()),
        usuario_id=usuario_id,
        curso_id=curso_id
    )
    db.add(new_inscricao)
    await db.commit()
    await db.refresh(new_inscricao)
    return new_inscricao

async def desinscrever_usuario_de_curso(db: AsyncSession, inscricao_id: str) -> bool:
    """
    Desinscreve um usuário de um curso.
    """
    stmt = delete(Inscricao).where(Inscricao.id == inscricao_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

async def listar_inscricoes_por_usuario(db: AsyncSession, usuario_id: str) -> List[Inscricao]:
    """
    Lista todas as inscrições de um usuário, incluindo os detalhes do curso.
    """
    stmt = (
        select(Inscricao)
        .where(Inscricao.usuario_id == usuario_id)
        .options(selectinload(Inscricao.curso)) # Eager load para incluir detalhes do curso
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def verificar_inscricao_existente(db: AsyncSession, usuario_id: str, curso_id: str) -> Inscricao | None:
    """
    Verifica se já existe uma inscrição para o usuário e curso especificados.
    """
    stmt = select(Inscricao).where(
        Inscricao.usuario_id == usuario_id,
        Inscricao.curso_id == curso_id
    )
    result = await db.execute(stmt)
    return result.scalars().first()
