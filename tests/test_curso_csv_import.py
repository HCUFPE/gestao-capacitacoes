import pytest
from src.controllers.curso_controller import importar_cursos_csv
from src.models import Curso
from sqlalchemy.future import select

@pytest.mark.asyncio
async def test_importar_cursos_csv_sucesso(db_session):
    csv_content = """id_curso;nome_curso;carga_horaria;eixos_tematicos
1;Curso 1;10;Tema 1
2;Curso 2;20;Tema 2
"""
    file_bytes = csv_content.encode('utf-8')
    
    result = await importar_cursos_csv(file_bytes, db_session)
    
    assert result["novos"] == 2
    assert result["atualizados"] == 0
    assert len(result["erros"]) == 0
    
    # Verify in DB
    cursos = (await db_session.execute(select(Curso))).scalars().all()
    assert len(cursos) == 2
    assert cursos[0].id == "1"
    assert cursos[0].titulo == "Curso 1"
    assert cursos[0].carga_horaria == 10
    assert cursos[0].tema == "Tema 1"

@pytest.mark.asyncio
async def test_importar_cursos_csv_upsert(db_session):
    # Setup initial course
    curso = Curso(id="1", titulo="Curso Antigo", carga_horaria=5)
    db_session.add(curso)
    await db_session.commit()
    
    csv_content = """id_curso;nome_curso;carga_horaria
1;Curso Atualizado;15
2;Novo Curso;30
"""
    file_bytes = csv_content.encode('utf-8')
    
    result = await importar_cursos_csv(file_bytes, db_session)
    
    assert result["novos"] == 1
    assert result["atualizados"] == 1
    assert len(result["erros"]) == 0
    
    # Verify in DB
    c1 = (await db_session.execute(select(Curso).where(Curso.id == "1"))).scalars().first()
    assert c1.titulo == "Curso Atualizado"
    assert c1.carga_horaria == 15
    
    c2 = (await db_session.execute(select(Curso).where(Curso.id == "2"))).scalars().first()
    assert c2 is not None

@pytest.mark.asyncio
async def test_importar_cursos_csv_iso_8859_1(db_session):
    csv_content = """id_curso;nome_curso
1;Comunicação e Ação
"""
    # encode as latin-1 / iso-8859-1
    file_bytes = csv_content.encode('iso-8859-1')
    
    result = await importar_cursos_csv(file_bytes, db_session)
    
    assert result["novos"] == 1
    assert result["atualizados"] == 0
    assert len(result["erros"]) == 0
    
    c1 = (await db_session.execute(select(Curso).where(Curso.id == "1"))).scalars().first()
    assert c1.titulo == "Comunicação e Ação"

@pytest.mark.asyncio
async def test_importar_cursos_csv_missing_columns(db_session):
    csv_content = """coluna_errada;outra_coluna
1;Teste
"""
    file_bytes = csv_content.encode('utf-8')
    
    result = await importar_cursos_csv(file_bytes, db_session)
    
    assert result["novos"] == 0
    assert result["atualizados"] == 0
    assert len(result["erros"]) > 0
    assert "Colunas obrigatórias" in result["erros"][0]
