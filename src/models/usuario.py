from sqlalchemy import Column, String, Enum
from .base import Base

import enum

class PerfilUsuario(enum.Enum):
    TRABALHADOR = "Trabalhador"
    CHEFIA = "Chefia"
    UDP = "UDP"

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(String, primary_key=True, doc="sAMAccountName do usuário no AD")
    nome = Column(String, nullable=False, doc="displayName do usuário no AD")
    email = Column(String, doc="Endereço de e-mail do usuário no AD")
    perfil = Column(Enum(PerfilUsuario), default=PerfilUsuario.TRABALHADOR, nullable=False)
    lotacao = Column(String, doc="Departamento do usuário, vindo do AD (em maiúsculas)")
    nome_chefia = Column(String, doc="Nome do chefe direto do usuário, vindo do AD (em maiúsculas)")
    cargo = Column(String, nullable=True, doc="Cargo do usuário, vindo do AD (title)")
    matricula = Column(String, nullable=True, doc="Matrícula do usuário, vindo do AD (employeeNumber)")
    cpf = Column(String, nullable=True, unique=True, doc="CPF do usuário")
    vinculo = Column(String, nullable=True, doc="Vínculo do usuário (RJU, EBSERH, etc.)")

    def __repr__(self):
        return f"<Usuario(id='{self.id}', nome='{self.nome}', perfil='{self.perfil.value}')>"
