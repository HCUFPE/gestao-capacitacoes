from sqlalchemy import Column, String, Integer, Enum
from ..resources.database import Base
import enum

class AnoGD(enum.Enum):
    ANO_2024 = 2024
    ANO_2025 = 2025
    ANO_2026 = 2026

class Curso(Base):
    __tablename__ = 'cursos'

    id = Column(String, primary_key=True)
    titulo = Column(String, nullable=False)
    certificadora = Column(String)
    carga_horaria = Column(Integer)
    link = Column(String)
    ano_gd = Column(Enum(AnoGD))
    # Armazena o ID da chefia que cadastrou o curso
    chefia_id = Column(String, nullable=False)
    # Armazena a lotação para a qual o curso se destina
    lotacao = Column(String, nullable=False)

    def __repr__(self):
        return f"<Curso(id='{self.id}', titulo='{self.titulo}')>"
