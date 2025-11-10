from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, select, func
import re
from typing import List, Dict, Any

from ..models import Usuario, PerfilUsuario, Atribuicao

async def sincronizar_usuario(db: AsyncSession, user_info: dict) -> Usuario:
    """
    Sincroniza os dados de um usuário do Active Directory com o banco de dados local.
    Se o usuário não existir, ele é criado com perfil 'Trabalhador'.
    Se existir, seus dados são atualizados, mas o perfil é preservado.
    """
    user_id = user_info.get("sAMAccountName", [None])[0]
    if not user_id:
        # Não deveria acontecer se a autenticação AD funcionou
        raise ValueError("sAMAccountName não encontrado nos dados do AD")

    # Busca o usuário existente
    stmt_select = select(Usuario).where(Usuario.id == user_id)
    result = await db.execute(stmt_select)
    db_user = result.scalars().first()

    # Extrai e trata os dados do AD
    display_name = user_info.get("displayName", [""])[0]
    email = user_info.get("mail", [""])[0]
    department = user_info.get("department", [""])[0].upper()
    
    # Extrai o nome do chefe do campo 'manager'
    manager_dn = user_info.get("manager", [None])[0]
    manager_name = ""
    if manager_dn:
        match = re.search(r'CN=([^,]+)', manager_dn)
        if match:
            manager_name = match.group(1).upper()

    if db_user:
        # Usuário existe, atualiza os dados
        stmt_update = (
            update(Usuario)
            .where(Usuario.id == user_id)
            .values(
                nome=display_name,
                email=email,
                lotacao=department,
                nome_chefia=manager_name
            )
        )
        await db.execute(stmt_update)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    else:
        # Usuário não existe, cria um novo
        new_user = Usuario(
            id=user_id,
            nome=display_name,
            email=email,
            lotacao=department,
            nome_chefia=manager_name,
            perfil=PerfilUsuario.TRABALHADOR # Perfil padrão
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

async def atualizar_perfil_usuario(db: AsyncSession, user_id: str, novo_perfil: PerfilUsuario) -> Usuario | None:
    """
    Atualiza o perfil de um usuário específico.
    """
    stmt = (
        update(Usuario)
        .where(Usuario.id == user_id)
        .values(perfil=novo_perfil)
        .returning(Usuario)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()

async def listar_usuarios(db: AsyncSession, nome: str | None = None, lotacao: str | None = None) -> List[Dict[str, Any]]:
    """
    Lista todos os usuários cadastrados no sistema, com filtros opcionais,
    incluindo a contagem de cursos atribuídos.
    """
    # Subquery para contar as atribuições por usuário
    subquery = (
        select(Atribuicao.user_id, func.count(Atribuicao.id).label("course_count"))
        .group_by(Atribuicao.user_id)
        .subquery()
    )

    # Query principal para buscar usuários e juntar com a contagem
    stmt = (
        select(
            Usuario,
            func.coalesce(subquery.c.course_count, 0).label("course_count")
        )
        .join_from(Usuario, subquery, Usuario.id == subquery.c.user_id, isouter=True)
        .order_by(Usuario.nome)
    )

    # Aplica filtros se fornecidos
    if nome:
        stmt = stmt.where(Usuario.nome.ilike(f"%{nome}%"))
    if lotacao:
        stmt = stmt.where(Usuario.lotacao.ilike(f"%{lotacao}%"))

    result = await db.execute(stmt)
    
    # Mapeia o resultado para um formato de dicionário
    users_with_counts = []
    for row in result:
        user_data = row.Usuario.__dict__
        user_data["course_count"] = row.course_count
        users_with_counts.append(user_data)
        
    print(f"DEBUG: listar_usuarios found {len(users_with_counts)} users.")
    return users_with_counts

async def listar_lotacoes_unicas(db: AsyncSession) -> List[str]:
    """
    Retorna uma lista de valores únicos de lotação da tabela de usuários.
    """
    stmt = select(Usuario.lotacao).distinct().order_by(Usuario.lotacao)
    result = await db.execute(stmt)
    return result.scalars().all()
