from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base

class Inscricao(Base):
    __tablename__ = 'inscricoes'

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('usuarios.id'), nullable=False)
    curso_id = Column(String, ForeignKey('cursos.id'), nullable=False)
    
    inscrito_em = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario")
    curso = relationship("Curso")

    def __repr__(self):
        return f"<Inscricao(id={self.id}, user_id='{self.user_id}', curso_id={self.curso_id})>"
