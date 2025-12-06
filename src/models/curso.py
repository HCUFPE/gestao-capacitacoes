from sqlalchemy import Column, Integer, String, DateTime, func, Boolean as saBoolean, Text
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

    # Novos campos da planilha
    conteudista = Column(String, nullable=True)
    disponibilidade_dias = Column(Integer, nullable=True)
    tipo_oferta = Column(String, nullable=True)
    apresentacao = Column(Text, nullable=True)
    publico_alvo = Column(Text, nullable=True)
    conteudo_programatico = Column(Text, nullable=True)
    data_lancamento = Column(String, nullable=True)
    acessibilidade = Column(String, nullable=True)
    observacao = Column(Text, nullable=True)

    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, onupdate=func.now())
