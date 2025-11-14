# src/providers/implementations/curso_provider.py
from ..interfaces.curso_provider_interface import CursoProviderInterface
from typing import List, Dict, Any

class CursoProvider(CursoProviderInterface):
    async def listar_cursos(self) -> List[Dict[str, Any]]:
        pass

    async def criar_curso(self, curso_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    async def atualizar_curso(self, curso_id: str, curso_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    async def deletar_curso(self, curso_id: str) -> bool:
        pass

    async def obter_curso_por_id(self, curso_id: str) -> Dict[str, Any]:
        pass

    async def listar_cursos_recomendados_por_lotacao(self, lotacao: str) -> List[Dict[str, Any]]:
        pass
