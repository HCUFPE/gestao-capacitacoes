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

async def listar_atribuicoes_por_usuario(db: AsyncSession, user_id: str) -> List[dict]:
    """
    Lista todas as atribuições de um usuário, incluindo os detalhes do curso.
    """
    stmt = (
        select(Atribuicao)
        .where(Atribuicao.user_id == user_id)
        .options(selectinload(Atribuicao.curso)) # Eager load para incluir detalhes do curso
    )
    result = await db.execute(stmt)
    atribuicoes = result.scalars().all()

    response_data = []
    for atribuicao in atribuicoes:
        if atribuicao.curso:
            atribuicao_data = {
                "id": atribuicao.id,
                "user_id": atribuicao.user_id,
                "curso_id": atribuicao.curso_id,
                "status": atribuicao.status,
                "atribuido_em": atribuicao.atribuido_em,
                "curso": {
                    "id": atribuicao.curso.id,
                    "titulo": atribuicao.curso.titulo,
                    "certificadora": atribuicao.curso.certificadora,
                    "carga_horaria": atribuicao.curso.carga_horaria,
                    "link": atribuicao.curso.link,
                    "ano_gd": atribuicao.curso.ano_gd,
                    "lotacao_id": atribuicao.curso.lotacao_id,
                }
            }
            response_data.append(atribuicao_data)
            
    return response_data

async def obter_atribuicao_por_id(db: AsyncSession, atribuicao_id: str) -> Atribuicao | None:
    """
    Obtém uma atribuição pelo ID, incluindo os detalhes do curso.
    """
    result = await db.execute(
        select(Atribuicao)
        .where(Atribuicao.id == atribuicao_id)
        .options(selectinload(Atribuicao.curso))
    )
    return result.scalars().first()

async def listar_atribuicoes_pendentes_validacao(db: AsyncSession, lotacao: str) -> List[dict]:
    """
    Lista atribuições com status 'REALIZADO' para uma lotação específica,
    aguardando validação.
    """
    stmt = (
        select(Atribuicao)
        .join(Usuario, Atribuicao.user_id == Usuario.id)
        .where(
            Atribuicao.status == StatusAtribuicao.REALIZADO,
            Usuario.lotacao == lotacao
        )
        .options(
            selectinload(Atribuicao.curso),
            selectinload(Atribuicao.user)
        )
        .order_by(Atribuicao.data_conclusao.asc())
    )
    result = await db.execute(stmt)
    atribuicoes = result.scalars().unique().all()

    # Estruturar a resposta para o frontend
    response = []
    for atribuicao in atribuicoes:
        response.append({
            "atribuicao_id": atribuicao.id,
            "data_submissao": atribuicao.data_conclusao,
            "usuario_nome": atribuicao.user.nome,
            "curso_titulo": atribuicao.curso.titulo,
            "certificado_id": atribuicao.certificado_id,
        })
    return response
