from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from datetime import datetime
from sqlalchemy.orm import selectinload
from uuid import uuid4
from typing import List

from ..models import Atribuicao, StatusAtribuicao, Usuario, Curso

async def criar_atribuicoes_para_lotacao(db: AsyncSession, curso_id: str, lotacao: str):
    """
    Cria registros de atribuição para todos os usuários de uma determinada lotação.
    """
    # 1. Encontrar todos os usuários na lotação especificada
    stmt_select_users = select(Usuario.id).where(Usuario.lotacao == lotacao)
    result = await db.execute(stmt_select_users)
    user_ids = result.scalars().all()

    if not user_ids:
        return # Nenhum usuário encontrado para esta lotação

    # 2. Criar uma lista de novas atribuições
    novas_atribuicoes = [
        Atribuicao(
            id=str(uuid4()),
            user_id=user_id,
            curso_id=curso_id,
            status=StatusAtribuicao.PENDENTE,
            data_atribuicao=datetime.utcnow()
        )
        for user_id in user_ids
    ]

    # 3. Adicionar todas as novas atribuições à sessão em lote
    db.add_all(novas_atribuicoes)
    await db.commit()

async def atualizar_atribuicao_com_certificado(
    db: AsyncSession,
    atribuicao_id: str,
    certificado_id: str,
    novo_status: StatusAtribuicao
):
    """
    Atualiza uma atribuição com o ID do certificado e um novo status.
    """
    stmt = (
        update(Atribuicao)
        .where(Atribuicao.id == atribuicao_id)
        .values(
            certificado_id=certificado_id,
            status=novo_status,
            data_conclusao=datetime.utcnow()
        )
    )
    await db.execute(stmt)
    await db.commit()

async def validar_atribuicao(
    db: AsyncSession,
    atribuicao_id: str,
    status: StatusAtribuicao
):
    """
    Valida ou recusa uma atribuição, atualizando seu status e data de validação.
    """
    stmt = (
        update(Atribuicao)
        .where(Atribuicao.id == atribuicao_id)
        .values(
            status=status,
            data_validacao=datetime.utcnow()
        )
    )
    await db.execute(stmt)
    await db.commit()

async def listar_atribuicoes_por_usuario(db: AsyncSession, user_id: str) -> List[Atribuicao]:
    """
    Lista todas as atribuições de um usuário, incluindo os detalhes do curso.
    """
    stmt = (
        select(Atribuicao)
        .where(Atribuicao.user_id == user_id)
        .options(selectinload(Atribuicao.curso)) # Eager load para incluir detalhes do curso
    )
    result = await db.execute(stmt)
    return result.scalars().all()
