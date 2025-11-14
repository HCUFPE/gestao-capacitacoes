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
    title = user_info.get("title", [""])[0]
    employee_number = user_info.get("employeeNumber", [""])[0]
    
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
                nome_chefia=manager_name,
                cargo=title,
                matricula=employee_number
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
            cargo=title,
            matricula=employee_number,
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

async def listar_usuarios(db: AsyncSession, nome: str | None = None, lotacao: str | None = None, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
    """
    Lista usuários de forma paginada, com filtros opcionais,
    incluindo a contagem de cursos atribuídos.
    """
    # Base query for filtering
    base_query = select(Usuario)
    if nome:
        base_query = base_query.where(Usuario.nome.ilike(f"%{nome}%"))
    if lotacao:
        base_query = base_query.where(Usuario.lotacao.ilike(f"%{lotacao}%"))

    # Query for total count
    count_stmt = select(func.count()).select_from(base_query.alias())
    total_count = (await db.execute(count_stmt)).scalar_one()

    # Subquery for course count
    subquery = (
        select(Atribuicao.user_id, func.count(Atribuicao.id).label("course_count"))
        .group_by(Atribuicao.user_id)
        .subquery()
    )

    # Main query for fetching paginated data
    data_stmt = (
        select(
            Usuario,
            func.coalesce(subquery.c.course_count, 0).label("course_count")
        )
        .join_from(Usuario, subquery, Usuario.id == subquery.c.user_id, isouter=True)
        .order_by(Usuario.nome)
        .offset(skip)
        .limit(limit)
    )
    
    # Apply filters to the data query as well
    if nome:
        data_stmt = data_stmt.where(Usuario.nome.ilike(f"%{nome}%"))
    if lotacao:
        data_stmt = data_stmt.where(Usuario.lotacao.ilike(f"%{lotacao}%"))

    result = await db.execute(data_stmt)
    
    # Map results to dictionary format
    users_with_counts = []
    for row in result:
        user_data = row.Usuario.__dict__
        user_data["course_count"] = row.course_count
        users_with_counts.append(user_data)
        
    print(f"DEBUG: listar_usuarios found {len(users_with_counts)} users for this page.")
    return {"total_count": total_count, "data": users_with_counts}

async def get_user_by_username(db: AsyncSession, username: str) -> Usuario | None:
    """
    Retorna um objeto Usuario pelo seu username (sAMAccountName), que é o ID no banco de dados.
    """
    stmt = select(Usuario).where(Usuario.id == username)
    result = await db.execute(stmt)
    return result.scalars().first()

async def listar_lotacoes_unicas(db: AsyncSession) -> List[str]:
    """
    Retorna uma lista de valores únicos de lotação da tabela de usuários,
    excluindo valores nulos.
    """
    try:
        stmt = (
            select(Usuario.lotacao)
            .where(Usuario.lotacao.isnot(None))
            .distinct()
            .order_by(Usuario.lotacao)
        )
        result = await db.execute(stmt)
        lotacoes = result.scalars().all()
        # Garante que mesmo uma string vazia não seja retornada, se existir.
        return [lotacao for lotacao in lotacoes if lotacao]
    except Exception as e:
        print(f"ERROR: Could not fetch unique lotacoes. Reason: {e}")
        # Em caso de erro, retorna uma lista vazia para não quebrar o frontend.
        return []
