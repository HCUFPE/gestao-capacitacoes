import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from src.models import Curso

async def main():
    engine = create_async_engine("sqlite+aiosqlite:///app.db")
    async with engine.connect() as conn:
        result = await conn.execute(select(Curso).where(Curso.lotacao == 'SETOR DE TECNOLOGIA DA INFORMAÇÃO E SAÚDE DIGITAL'))
        cursos = result.fetchall()
        if cursos:
            for curso in cursos:
                print(curso)
        else:
            print("No recommended courses found")

if __name__ == "__main__":
    asyncio.run(main())
