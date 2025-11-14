from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime

class StatusAtribuicao(str, enum.Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluído"
    REALIZADO = "REALIZADO"

class Atribuicao(Base):
    __tablename__ = 'atribuicoes'

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('usuarios.id'), nullable=False)
    curso_id = Column(String, ForeignKey('cursos.id'), nullable=False)
    status = Column(Enum(StatusAtribuicao), default=StatusAtribuicao.PENDENTE)
    atribuido_em = Column(DateTime, default=datetime.utcnow)
    criado_por_usuario = Column(Boolean, default=False, nullable=False)
    certificado_id = Column(String, ForeignKey('certificados.id'), nullable=True) # New column
    data_conclusao = Column(DateTime, nullable=True) # New column

    user = relationship("Usuario")
    curso = relationship("Curso")
    certificado = relationship("Certificado") # New relationship

    def __repr__(self):
        return f"<Atribuicao(id={self.id}, user_id='{self.user_id}', curso_id={self.curso_id}, status='{self.status.value}')>"
