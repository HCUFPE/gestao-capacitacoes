from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
from uuid import uuid4

class Inscricao(Base):
    __tablename__ = 'inscricoes'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    usuario_id = Column(String, ForeignKey('usuarios.id'), nullable=False)
    curso_id = Column(String, ForeignKey('cursos.id'), nullable=False)
    data_inscricao = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")
    curso = relationship("Curso")
