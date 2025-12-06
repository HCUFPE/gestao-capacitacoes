from abc import ABC, abstractmethod
from typing import List, Dict, Any

class RelatorioProviderInterface(ABC):
    """
    Interface para o provedor de dados de relatórios.
    Define os métodos para obter dados necessários para a geração de relatórios
    de capacitações EAD.
    """

    @abstractmethod
    async def listar_dados_capacitacoes(self) -> List[Dict[str, Any]]:
        """
        Retorna uma lista de dicionários contendo todos os dados detalhados
        para o relatório de capacitações, incluindo informações de usuário, curso e certificado.
        """
        pass

    @abstractmethod
    async def get_status_lotacao(self, lotacao: str) -> List[Dict[str, Any]]:
        """
        Retorna o status consolidado das atribuições para uma lotação específica (KPIs).
        """
        pass

    @abstractmethod
    async def get_progresso_equipe(self, lotacao: str) -> List[Dict[str, Any]]:
        """
        Retorna o progresso individual detalhado dos membros da equipe da lotação.
        """
        pass
