import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def main():
    engine = create_async_engine("sqlite+aiosqlite:///app.db")
    async with engine.connect() as conn:
        print("--- Usuarios (Cargo) ---")
        try:
            result = await conn.execute(text("SELECT id, nome, cargo FROM usuarios LIMIT 5"))
            rows = result.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error querying usuarios: {e}")

        print("\n--- Cursos (Certificadora) ---")
        try:
            result = await conn.execute(text("SELECT id, titulo, certificadora FROM cursos LIMIT 5"))
            rows = result.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error querying cursos: {e}")

if __name__ == "__main__":
    asyncio.run(main())

