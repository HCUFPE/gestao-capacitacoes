# src/providers/interfaces/curso_provider_interface.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class CursoProviderInterface(ABC):
    @abstractmethod
    async def listar_cursos(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def criar_curso(self, curso_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def atualizar_curso(self, curso_id: str, curso_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def deletar_curso(self, curso_id: str) -> bool:
        pass

    @abstractmethod
    async def obter_curso_por_id(self, curso_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def listar_cursos_recomendados_por_lotacao(self, lotacao: str) -> List[Dict[str, Any]]:
        pass
