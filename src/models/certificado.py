from sqlalchemy import Column, String, Integer, Boolean
from .base import Base

class Certificado(Base):
    __tablename__ = 'certificados'

    id = Column(String, primary_key=True)
    file_path = Column(String, doc="Caminho do arquivo de certificado salvo localmente")
    link = Column(String, doc="Link para o certificado externo")
    validado = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Certificado(id='{self.id}', validado={self.validado})>"
