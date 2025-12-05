from sqlalchemy import Column, Integer, String, DateTime, func, Boolean as saBoolean
from .base import Base

class Curso(Base):
    __tablename__ = 'cursos'
    id = Column(String, primary_key=True)
    titulo = Column(String, nullable=False)
    certificadora = Column(String)
    carga_horaria = Column(Integer)
    link = Column(String)
    tema = Column(String, nullable=True, doc="Tema ou categoria do curso") # NOVO: Campo para Tema do curso
    ano_gd = Column(String) # Changed from Enum to String
    lotacao_id = Column(String) # ID da lotação/setor no AD
    atribuir_a_todos = Column(saBoolean, default=False)

    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, onupdate=func.now())
