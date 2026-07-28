from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List, Dict, Any, Tuple
from uuid import uuid4
import csv
import io

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

async def importar_cursos_csv(file_bytes: bytes, db: AsyncSession) -> Dict[str, Any]:
    """
    Importa cursos a partir de um arquivo CSV, realizando Upsert.
    """
    try:
        content = file_bytes.decode('utf-8')
    except UnicodeDecodeError:
        content = file_bytes.decode('iso-8859-1')
        
    stream = io.StringIO(content)
    # Tenta descobrir o delimitador
    primeira_linha = stream.readline()
    if not primeira_linha:
        return {"novos": 0, "atualizados": 0, "erros": ["Arquivo vazio."]}
        
    delimitador = ';' if ';' in primeira_linha else ','
    stream.seek(0)
    
    reader = csv.DictReader(stream, delimiter=delimitador)
    
    if not reader.fieldnames or 'id_curso' not in reader.fieldnames or 'nome_curso' not in reader.fieldnames:
        return {"novos": 0, "atualizados": 0, "erros": ["Colunas obrigatórias 'id_curso' ou 'nome_curso' não encontradas."]}
        
    novos = 0
    atualizados = 0
    erros = []
    
    COLUMN_MAP = {
        'id_curso': 'id',
        'nome_curso': 'titulo',
        'Link': 'link',
        'eixos_tematicos': 'tema',
        'certificador': 'certificadora',
        'conteudista': 'conteudista',
        'carga_horaria': 'carga_horaria',
        'disponibilidade_dias': 'disponibilidade_dias',
        'tipo_oferta': 'tipo_oferta',
        'apresentacao': 'apresentacao',
        'publico_alvo': 'publico_alvo',
        'conteudo_programatico': 'conteudo_programatico',
        'data_lancamento': 'data_lancamento',
        'Acessibilidade': 'acessibilidade',
        'Observacao': 'observacao'
    }

    for row_num, row in enumerate(reader, start=2): # +1 para header, +1 para 1-index
        id_curso = row.get('id_curso', '').strip()
        nome_curso = row.get('nome_curso', '').strip()
        
        if not id_curso or not nome_curso:
            erros.append(f"Linha {row_num}: 'id_curso' ou 'nome_curso' ausentes.")
            continue
            
        curso_kwargs = {}
        for csv_col, db_col in COLUMN_MAP.items():
            val = row.get(csv_col)
            if val is not None:
                val = val.strip()
                if db_col in ['carga_horaria', 'disponibilidade_dias']:
                    try:
                        val = int(val) if val else None
                    except ValueError:
                        val = None
                curso_kwargs[db_col] = val
                
        # Upsert logic
        result = await db.execute(select(Curso).where(Curso.id == id_curso))
        curso_existente = result.scalars().first()
        
        try:
            if curso_existente:
                atualizou = False
                for k, v in curso_kwargs.items():
                    # Ignorar id na atualização
                    if k != 'id' and getattr(curso_existente, k) != v:
                        setattr(curso_existente, k, v)
                        atualizou = True
                if atualizou:
                    atualizados += 1
            else:
                novo_curso = Curso(**curso_kwargs)
                db.add(novo_curso)
                novos += 1
        except Exception as e:
            erros.append(f"Linha {row_num}: Erro ao processar curso {id_curso}: {str(e)}")
            
    await db.commit()
    
    return {
        "novos": novos,
        "atualizados": atualizados,
        "erros": erros
    }
