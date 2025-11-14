# src/providers/interfaces/certificado_provider_interface.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class CertificadoProviderInterface(ABC):
    @abstractmethod
    async def registrar_certificado(self, certificado_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def validar_certificado(self, certificado_id: str, status: str) -> bool:
        pass

    @abstractmethod
    async def listar_certificados_por_usuario(self, usuario_id: str) -> List[Dict[str, Any]]:
        pass
