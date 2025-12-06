import asyncio
import os
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models import Usuario, Curso, Atribuicao, Certificado, StatusAtribuicao, PerfilUsuario

# Config
DATABASE_URL = os.getenv("SQLITE_DSN", "sqlite+aiosqlite:///./app.db")
LOTACAO_TESTE = "UNIDADE DE DESENVOLVIMENTO DE PESSOAL"

async def populate():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        print("--- Criando dados de teste ---")

        # 1. Criar Usuário de Teste
        user_id = "user.teste"
        user = Usuario(
            id=user_id,
            nome="Usuário Teste da Silva",
            email="teste@exemplo.com",
            perfil=PerfilUsuario.TRABALHADOR,
            lotacao=LOTACAO_TESTE,
            cargo="Analista Testador"
        )
        session.add(user) # Se já existir vai dar erro, vamos tratar ou usar merge?
        # Usar merge para ser idempotente (simplificado)
        await session.merge(user)
        print(f"Usuário {user_id} preparado.")

        # 2. Criar Curso de Teste
        curso_id = str(uuid4())
        curso = Curso(
            id=curso_id,
            titulo="Curso de Compliance e Ética",
            certificadora="Escola Corporativa",
            carga_horaria=20,
            ano_gd="2025"
        )
        session.add(curso)
        print(f"Curso '{curso.titulo}' criado.")

        # 3. Criar Certificado (Simulado)
        cert_id = str(uuid4())
        certificado = Certificado(
            id=cert_id,
            curso_id=curso_id,
            link="https://exemplo.com/certificado_teste.pdf",
            validado=False
        )
        session.add(certificado)

        # 4. Criar Atribuição (Status REALIZADO = Pendente de Validação)
        atribuicao = Atribuicao(
            id=str(uuid4()),
            user_id=user_id,
            curso_id=curso_id,
            status=StatusAtribuicao.REALIZADO, # IMPORTANTE: Status que aparece na validação
            atribuido_em=datetime.utcnow(),
            certificado_id=cert_id,
            data_conclusao=datetime.utcnow()
        )
        session.add(atribuicao)
        print(f"Atribuição criada com status REALIZADO para {user_id}.")

        await session.commit()
        print("--- Dados persistidos com sucesso! ---")

if __name__ == "__main__":
    asyncio.run(populate())
