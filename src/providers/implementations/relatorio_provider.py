from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ..interfaces.relatorio_provider_interface import RelatorioProviderInterface
from ...models import Usuario, Curso, Atribuicao, Certificado

class RelatorioProvider(RelatorioProviderInterface):
    """
    Implementação do provedor de dados de relatórios usando SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def listar_dados_capacitacoes(self) -> List[Dict[str, Any]]:
        """
        Retorna uma lista de dicionários contendo todos os dados detalhados
        para o relatório de capacitações.
        """
        # Define a query principal, começando por Atribuicao para ligar Usuario e Curso
        query = (
            select(
                Usuario.cpf,
                Usuario.vinculo,
                Usuario.lotacao.label("setor"),
                Usuario.nome.label("nome_profissional"),
                Curso.ano_gd,
                Curso.titulo.label("nome_curso"),
                Curso.carga_horaria,
                Curso.certificadora.label("plataforma"),
                Curso.tema,
                Certificado.file_path.label("certificado_path"),
            )
            .join(Usuario, Atribuicao.user_id == Usuario.id)
            .join(Curso, Atribuicao.curso_id == Curso.id)
            .outerjoin(Certificado, Atribuicao.certificado_id == Certificado.id) # LEFT JOIN para incluir cursos sem certificado
        )
        
        result = await self.session.execute(query)
        
        report_data = []
        for row in result.mappings():
            # Mapeia o resultado para o formato desejado, tratando a presença do certificado
            data = dict(row)
            data["certificado"] = "Sim" if data["certificado_path"] else "Não"
            del data["certificado_path"] # Remove o path interno do relatório final
            report_data.append(data)
            
        return report_data
