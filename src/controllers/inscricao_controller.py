from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, func
from sqlalchemy.orm import selectinload, aliased
from uuid import uuid4
from typing import List, Tuple

from ..models import Inscricao, Curso, Usuario, Atribuicao, StatusAtribuicao, Certificado
from datetime import datetime

async def verificar_inscricao_existente(db: AsyncSession, usuario_id: str, curso_id: str) -> Inscricao | None:
    """
    Verifica se já existe uma inscrição para um usuário em um curso específico.
    """
    stmt = select(Inscricao).where(
        Inscricao.user_id == usuario_id,
        Inscricao.curso_id == curso_id
    )
    result = await db.execute(stmt)
    return result.scalars().first()

async def inscrever_usuario_em_curso(db: AsyncSession, usuario_id: str, curso_id: str) -> Tuple[Inscricao, Atribuicao]:
    """
    Inscreve um usuário em um curso.
    Se já existir uma atribuição 'Pendente' para este curso, atualiza seu status para 'Realizado'.
    Caso contrário, cria uma nova atribuição com status 'Realizado'.
    """
    # 1. Cria a inscrição
    new_inscricao = Inscricao(
        id=str(uuid4()),
        user_id=usuario_id,
        curso_id=curso_id
    )
    db.add(new_inscricao)

    # 2. Procura por uma atribuição existente
    stmt_select = select(Atribuicao).where(
        Atribuicao.user_id == usuario_id,
        Atribuicao.curso_id == curso_id
    )
    result = await db.execute(stmt_select)
    existing_atribuicao = result.scalars().first()

    if existing_atribuicao and existing_atribuicao.status == StatusAtribuicao.PENDENTE:
        # Atualiza a atribuição existente
        existing_atribuicao.status = StatusAtribuicao.EM_ANDAMENTO
        atribuicao_a_retornar = existing_atribuicao
    else:
        # Cria uma nova atribuição se não houver uma pendente
        new_atribuicao = Atribuicao(
            id=str(uuid4()),
            user_id=usuario_id,
            curso_id=curso_id,
            status=StatusAtribuicao.EM_ANDAMENTO, # Status 'Em Andamento' pois a inscrição está sendo feita
            criado_por_usuario=True # Marcado como criado por usuário
        )
        db.add(new_atribuicao)
        atribuicao_a_retornar = new_atribuicao

    await db.commit()
    
    # Eagerly load the relationship to avoid MissingGreenlet error
    result_inscricao = await db.execute(
        select(Inscricao)
        .where(Inscricao.id == new_inscricao.id)
        .options(selectinload(Inscricao.curso))
    )
    
    # Refresh a atribuição para garantir que temos o estado mais recente
    await db.refresh(atribuicao_a_retornar)

    return result_inscricao.scalar_one(), atribuicao_a_retornar

async def desinscrever_usuario_de_curso(db: AsyncSession, inscricao_id: str) -> bool:
    """
    Desinscreve um usuário de um curso e remove a atribuição associada.
    """
    # Encontrar a inscrição para obter o curso_id e usuario_id
    inscricao = await db.execute(select(Inscricao).where(Inscricao.id == inscricao_id))
    inscricao = inscricao.scalar_one_or_none()

    if not inscricao:
        return False

    # Encontrar a atribuição associada e reverter o status para 'Pendente'
    stmt_select_atribuicao = select(Atribuicao).where(
        Atribuicao.user_id == inscricao.user_id,
        Atribuicao.curso_id == inscricao.curso_id
    )
    result_atribuicao = await db.execute(stmt_select_atribuicao)
    atribuicao_a_reverter = result_atribuicao.scalars().first()

    if atribuicao_a_reverter:
        if atribuicao_a_reverter.criado_por_usuario:
            # Se a atribuição foi criada pelo usuário, deleta
            await db.delete(atribuicao_a_reverter)
        else:
            # Se a atribuição foi criada por um gestor, verifica o status do curso
            # para ver se a atribuição ainda é válida
            curso_associado = await db.execute(select(Curso).where(Curso.id == atribuicao_a_reverter.curso_id))
            curso_associado = curso_associado.scalars().first()

            if curso_associado and not curso_associado.atribuir_a_todos:
                # Se o curso não está mais atribuído a todos, deleta a atribuição
                await db.delete(atribuicao_a_reverter)
            else:
                # Caso contrário, reverte o status para Pendente
                atribuicao_a_reverter.status = StatusAtribuicao.PENDENTE
                db.add(atribuicao_a_reverter)

    # Remover a inscrição
    await db.delete(inscricao)
    await db.commit()
    return True

async def listar_inscricoes_por_usuario(db: AsyncSession, usuario_id: str) -> List[dict]:
    """
    Lista todas as inscrições de um usuário, incluindo os detalhes do curso e o status da atribuição.
    """
    # Alias para a tabela Atribuicao para evitar conflitos de nome
    AtribuicaoAlias = aliased(Atribuicao)
    CertificadoAlias = aliased(Certificado) # Alias para a tabela Certificado

    stmt = (
        select(
            Inscricao,
            AtribuicaoAlias.id.label("atribuicao_id"),
            AtribuicaoAlias.status.label("status"),
            CertificadoAlias.id.label("certificado_id"),
            CertificadoAlias.file_path.label("certificado_file_path"),
            CertificadoAlias.link.label("certificado_link")
        )
        .join(AtribuicaoAlias, (Inscricao.user_id == AtribuicaoAlias.user_id) & (Inscricao.curso_id == AtribuicaoAlias.curso_id))
        .outerjoin(CertificadoAlias, AtribuicaoAlias.certificado_id == CertificadoAlias.id) # LEFT JOIN com Certificado
        .where(Inscricao.user_id == usuario_id)
        .options(selectinload(Inscricao.curso)) # Eager load para incluir detalhes do curso
    )
    
    # DEBUG: Imprimir a consulta SQL gerada
    from sqlalchemy.dialects import sqlite
    print("SQL Query:", stmt.compile(dialect=sqlite.dialect()))
    
    result = await db.execute(stmt)
    
    # DEBUG: Imprimir o resultado bruto
    raw_results = result.all()
    print("Raw Results:", raw_results)
    
    inscricoes_com_status = []
    for inscricao, atribuicao_id, status, certificado_id, certificado_file_path, certificado_link in raw_results:
        if inscricao.curso:
            inscricao_data = {
                "id": inscricao.id,
                "user_id": inscricao.user_id,
                "curso_id": inscricao.curso_id,
                "inscrito_em": inscricao.inscrito_em,
                "atribuicao_id": atribuicao_id,
                "status": status,
                "certificado_id": certificado_id,
                "certificado_file_path": certificado_file_path,
                "certificado_link": certificado_link,
                "curso": {
                    "id": inscricao.curso.id,
                    "titulo": inscricao.curso.titulo,
                    "certificadora": inscricao.curso.certificadora,
                    "carga_horaria": inscricao.curso.carga_horaria,
                    "link": inscricao.curso.link,
                    "ano_gd": inscricao.curso.ano_gd,
                    "lotacao_id": inscricao.curso.lotacao_id,
                }
            }
            inscricoes_com_status.append(inscricao_data)
    
    return inscricoes_com_status
