from sqlalchemy import Column, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime

class StatusAtribuicao(enum.Enum):
    PENDENTE = "Pendente"
    REALIZADO = "Realizado"
    VALIDADO = "Validado"
    RECUSADO = "Recusado" # Adicionado para cobrir cenários de validação

class Atribuicao(Base):
    __tablename__ = 'atribuicoes'

    id = Column(String, primary_key=True) # Pode ser um UUID gerado automaticamente
    user_id = Column(String, ForeignKey('usuarios.id'), nullable=False)
    curso_id = Column(String, ForeignKey('cursos.id'), nullable=False)
    status = Column(Enum(StatusAtribuicao), default=StatusAtribuicao.PENDENTE, nullable=False)
    certificado_id = Column(String, ForeignKey('certificados.id'), nullable=True) # Pode ser nulo se ainda não houver certificado

    data_atribuicao = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_conclusao = Column(DateTime, doc="Data em que o usuário marcou como realizado")
    data_validacao = Column(DateTime, doc="Data em que a chefia/UDP validou o certificado")

    # Relacionamentos
    usuario = relationship("Usuario", backref="atribuicoes")
    curso = relationship("Curso", backref="atribuicoes")
    certificado = relationship("Certificado", backref="atribuicao", uselist=False) # Um certificado pertence a uma atribuição

    def __repr__(self):
        return f"<Atribuicao(id='{self.id}', user_id='{self.user_id}', curso_id='{self.curso_id}', status='{self.status.value}')>"
