import asyncio
import csv
import os
from dotenv import load_dotenv
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from src.resources.database import DatabaseManager
from src.models import Usuario, PerfilUsuario

# Carrega variáveis de ambiente imediatamente
load_dotenv()

# --- Configuration ---
CSV_FILE_PATH = 'usuarios.csv'
SQL_FILE_PATH = 'src/providers/sql/funcionarios/funcionarios.sql'
APP_DB_URL = os.getenv("SQLITE_DSN", "sqlite+aiosqlite:///./app.db")
# Tenta pegar POSTGRES_DSN, se não existir, tenta EXTERNAL_DB_DSN
EXTERNAL_DB_URL = os.getenv("POSTGRES_DSN", os.getenv("EXTERNAL_DB_DSN"))

async def get_sql_query():
    """Lê o arquivo SQL se ele existir e não estiver vazio."""
    if os.path.exists(SQL_FILE_PATH):
        with open(SQL_FILE_PATH, 'r') as f:
            content = f.read().strip()
            if content:
                return content
    return None

async def fetch_users_from_sql(query):
    """Executa a query no banco externo."""
    if not EXTERNAL_DB_URL:
        print("ERRO: Arquivo SQL encontrado, mas EXTERNAL_DB_DSN (ou POSTGRES_DSN) não está definido no .env.")
        return []
    
    print(f"Conectando ao banco externo: {EXTERNAL_DB_URL}")
    try:
        engine = create_async_engine(EXTERNAL_DB_URL)
        async with engine.connect() as conn:
            print("Executando query...")
            result = await conn.execute(text(query))
            rows = result.mappings().all()
            print(f"Query retornou {len(rows)} registros.")
            return rows
    except Exception as e:
        print(f"Erro ao executar SQL externo: {e}")
        return []
    finally:
        await engine.dispose()

async def import_users():
    print("--- Iniciando processo de importação de usuários ---")
    
    sql_query = await get_sql_query()
    users_data = []
    source_type = "CSV"

    if sql_query:
        print(f"Arquivo SQL detectado em: {SQL_FILE_PATH}")
        rows = await fetch_users_from_sql(sql_query)
        if rows:
            users_data = rows
            source_type = "SQL"
        else:
            print("Nenhum dado retornado do SQL ou erro de conexão. Tentando CSV...")
    
    if not users_data:
        if os.path.exists(CSV_FILE_PATH):
            print(f"Lendo arquivo CSV: {CSV_FILE_PATH}")
            with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                users_data = list(reader)
        else:
            print(f"Arquivo CSV não encontrado em {CSV_FILE_PATH}.")
            return

    if not users_data:
        print("Nenhum dado de usuário encontrado para importar.")
        return

    print(f"Processando {len(users_data)} registros ({source_type})...")
    
    db_manager = DatabaseManager(APP_DB_URL)
    
    async for db in db_manager.get_session():
        count_new = 0
        count_updated = 0
        
        for row in users_data:
            # Normalização de chaves (id, nome, email, cpf, vinculo)
            # Tenta chaves comuns de retorno SQL ou CSV
            user_id = row.get('id') or row.get('sAMAccountName')
            
            # DEBUG SPECIFIC USER
            if user_id and 'filipe.cavalcanti' in str(user_id).lower():
                print(f"DEBUG: Found user in SQL result: {user_id}")
                print(f"DEBUG: Row data: {row}")
            
            if not user_id:
                continue

            nome = row.get('nome') or row.get('displayName')
            email = row.get('email') or row.get('mail')
            cpf = row.get('cpf')
            vinculo = row.get('vinculo')
            
            # Campos opcionais que podem vir da query
            lotacao = row.get('lotacao')
            cargo = row.get('cargo')
            matricula = row.get('matricula')

            # Verificar existência
            stmt = select(Usuario).where(Usuario.id == user_id)
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()

            if existing_user:
                # Atualiza dados se fornecidos e diferentes
                updated = False
                if cpf and existing_user.cpf != cpf:
                    existing_user.cpf = cpf
                    updated = True
                if vinculo and existing_user.vinculo != vinculo:
                    existing_user.vinculo = vinculo
                    updated = True
                if matricula and existing_user.matricula != matricula:
                    existing_user.matricula = matricula
                    updated = True
                # Atualiza outros campos apenas se estiverem vazios ou se quisermos forçar
                # Por enquanto, apenas CPF/Vinculo/Matricula são prioritários neste update
                
                if updated:
                    count_updated += 1
            else:
                # Insere novo usuário
                new_user = Usuario(
                    id=user_id,
                    nome=nome,
                    email=email,
                    perfil=PerfilUsuario.TRABALHADOR,
                    cpf=cpf,
                    vinculo=vinculo,
                    lotacao=lotacao,
                    cargo=cargo,
                    matricula=matricula
                )
                db.add(new_user)
                count_new += 1
        
        try:
            await db.commit()
            print(f"Importação concluída com sucesso!")
            print(f"Novos usuários: {count_new}")
            print(f"Usuários atualizados: {count_updated}")
        except IntegrityError as e:
            print(f"Erro de integridade no banco: {e}")
            await db.rollback()
        except Exception as e:
            print(f"Erro ao salvar no banco: {e}")
            await db.rollback()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    asyncio.run(import_users())