from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Certificado(Base):
    __tablename__ = 'certificados'

    id = Column(String, primary_key=True)
    curso_id = Column(String, ForeignKey('cursos.id'), nullable=False) # Add curso_id
    file_path = Column(String, doc="Caminho do arquivo de certificado salvo localmente")
    link = Column(String, doc="Link para o certificado externo")
    validado = Column(Boolean, default=False, nullable=False)

    curso = relationship("Curso") # Add relationship

    def __repr__(self):
        return f"<Certificado(id='{self.id}', curso_id='{self.curso_id}', validado={self.validado})>"
