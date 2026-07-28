from abc import ABC, abstractmethod
from typing import List, Dict, Any

class RelatorioProviderInterface(ABC):
    """
    Interface para o provedor de dados de relatórios.
    Define os métodos para obter dados necessários para a geração de relatórios
    de capacitações EAD.
    """

    @abstractmethod
    async def listar_dados_capacitacoes(
        self,
        ano: str | None = None,
        vinculo: str | None = None
    ) -> List[Dict[str, Any]]:
        """
        Retorna uma lista de dicionários contendo todos os dados detalhados
        para o relatório de capacitações, incluindo informações de usuário, curso e certificado.
        Suporta filtros opcionais por ano e vínculo.
        """
        pass

    @abstractmethod
    async def get_status_lotacao(
        self,
        lotacao: str,
        ano: str | None = None,
        vinculo: str | None = None
    ) -> List[Dict[str, Any]]:
        """
        Retorna o status consolidado das atribuições para uma lotação específica (KPIs).
        Suporta filtros opcionais por ano e vínculo.
        """
        pass

    @abstractmethod
    async def get_progresso_equipe(
        self,
        lotacao: str,
        ano: str | None = None,
        vinculo: str | None = None
    ) -> List[Dict[str, Any]]:
        """
        Retorna o progresso individual detalhado dos membros da equipe da lotação.
        Suporta filtros opcionais por ano e vínculo.
        """
        pass
