from sqlalchemy import Column, String, Enum
from ..resources.database import Base # Corrected import

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

    def __repr__(self):
        return f"<Usuario(id='{self.id}', nome='{self.nome}', perfil='{self.perfil.value}')>"
