import asyncio
import csv
import os
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from src.resources.database import DatabaseManager
from src.models import Usuario, PerfilUsuario

# --- Configuration ---
CSV_FILE_PATH = 'usuarios.csv'
DATABASE_URL = os.getenv("SQLITE_DSN", "sqlite+aiosqlite:///./app.db")

async def import_users_from_csv():
    """
    Reads a CSV file and pre-populates the 'usuarios' table.
    Skips users that already exist based on their ID.
    """
    print("Starting user import process...")
    
    db_manager = DatabaseManager(DATABASE_URL)
    
    # We need to manage the session manually for a script
    async for db in db_manager.get_session():
        
        # Get all existing user IDs to prevent duplicates
        existing_users_stmt = select(Usuario.id)
        existing_users_result = await db.execute(existing_users_stmt)
        existing_user_ids = {user_id for user_id, in existing_users_result}
        print(f"Found {len(existing_user_ids)} existing users in the database.")

        users_to_add = []
        
        try:
            with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    user_id = row.get('id')
                    
                    if not user_id:
                        print(f"Skipping row with no ID: {row}")
                        continue
                        
                    if user_id in existing_user_ids:
                        # print(f"Skipping existing user: {user_id}")
                        continue

                    # Handle potentially empty email
                    email = row.get('email')
                    if not email or email.isspace():
                        email = None

                    new_user = Usuario(
                        id=user_id,
                        nome=row.get('nome'),
                        email=email,
                        perfil=PerfilUsuario.TRABALHADOR, # Default profile
                        lotacao=None, # To be updated on first login
                        nome_chefia=None # To be updated on first login
                    )
                    users_to_add.append(new_user)
                    existing_user_ids.add(user_id) # Add to set to handle duplicates within the CSV

        except FileNotFoundError:
            print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
            return
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
            return

        if not users_to_add:
            print("No new users to import.")
            return

        print(f"Found {len(users_to_add)} new users to import from the CSV.")
        
        try:
            db.add_all(users_to_add)
            await db.commit()
            print(f"Successfully imported {len(users_to_add)} new users.")
        except IntegrityError as e:
            print(f"Database integrity error: {e}. This might happen with concurrent runs. Rolling back.")
            await db.rollback()
        except Exception as e:
            print(f"An error occurred during database insertion: {e}")
            await db.rollback()

if __name__ == "__main__":
    # Load environment variables to get the DSN
    from dotenv import load_dotenv
    load_dotenv()
    
    asyncio.run(import_users_from_csv())
