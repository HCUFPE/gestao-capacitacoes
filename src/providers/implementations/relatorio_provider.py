from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from sqlalchemy.orm import selectinload

from ..interfaces.relatorio_provider_interface import RelatorioProviderInterface
from ...models import Usuario, Curso, Atribuicao, Certificado

class RelatorioProvider(RelatorioProviderInterface):
    """
    Implementação do provedor de dados de relatórios usando SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def listar_dados_capacitacoes(
        self,
        ano: str | None = None,
        vinculo: str | None = None
    ) -> List[Dict[str, Any]]:
        """
        Retorna uma lista de dicionários contendo todos os dados detalhados
        para o relatório de capacitações.
        Suporta filtros opcionais por ano e vínculo.
        """
        # Define a query principal, começando por Atribuicao para ligar Usuario e Curso
        query = (
            select(
                Usuario.id,
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
            .select_from(Atribuicao) # Define explicitamente o ponto de partida da query
            .join(Usuario, Atribuicao.user_id == Usuario.id)
            .join(Curso, Atribuicao.curso_id == Curso.id)
            .outerjoin(Certificado, Atribuicao.certificado_id == Certificado.id) # LEFT JOIN para incluir cursos sem certificado
        )

        # Aplicar filtro por vínculo
        if vinculo:
            query = query.where(Usuario.vinculo == vinculo)

        # Aplicar filtro por ano
        if ano:
            query = query.where(Curso.ano_gd == str(ano))
        
        result = await self.session.execute(query)
        
        report_data = []
        for row in result.mappings():
            # Mapeia o resultado para o formato desejado, tratando a presença do certificado
            data = dict(row)
            data["certificado"] = "Sim" if data["certificado_path"] else "Não"
            del data["certificado_path"] # Remove o path interno do relatório final
            report_data.append(data)
            
        return report_data

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
        query = (
            select(
                Atribuicao.status,
                func.count(Atribuicao.id).label("total")
            )
            .join(Usuario, Atribuicao.user_id == Usuario.id)
            .where(Usuario.lotacao == lotacao)
        )

        if vinculo:
            query = query.where(Usuario.vinculo == vinculo)

        # Filtro por ano via data_conclusao
        if ano:
            query = query.where(func.strftime('%Y', Atribuicao.data_conclusao) == str(ano))

        query = query.group_by(Atribuicao.status)
        result = await self.session.execute(query)
        
        return [{"name": row.status.value if hasattr(row.status, 'value') else row.status, "value": row.total} for row in result.all()]

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
        # Calcula o progresso por usuário no setor
        # Status considerados concluídos: 'Realizado', 'Concluído', 'Validado'
        stmt = (
            select(
                Usuario.id,
                Usuario.nome,
                Usuario.matricula,
                Usuario.cargo,
                Usuario.vinculo,
                func.count(Atribuicao.id).label("total_atribuicoes"),
                func.sum(
                    case(
                        (Atribuicao.status.in_(['Realizado', 'Concluído', 'Validado']), 1),
                        else_=0
                    )
                ).label("total_concluido")
            )
            .outerjoin(Atribuicao, Usuario.id == Atribuicao.user_id)
            .where(Usuario.lotacao == lotacao)
        )

        # Aplicar filtro por ano (usando data_conclusao da Atribuicao)
        if ano:
            stmt = stmt.outerjoin(
                Atribuicao, (Usuario.id == Atribuicao.user_id) & (Atribuicao.data_conclusao != None)
            )

        # Aplicar filtro por vínculo
        if vinculo:
            stmt = stmt.where(Usuario.vinculo == vinculo)

        stmt = stmt.group_by(Usuario.id, Usuario.nome, Usuario.matricula, Usuario.cargo, Usuario.vinculo)

        result = await self.session.execute(stmt)

        team_progress = []
        for row in result.all():
            total = row.total_atribuicoes or 0
            concluido = row.total_concluido or 0
            progresso = (concluido / total * 100) if total > 0 else 0.0

            vinculo_display = row.vinculo if row.vinculo else "Não informado"

            team_progress.append({
                "id": row.id,
                "nome": row.nome,
                "matricula": row.matricula,
                "cargo": row.cargo,
                "vinculo": vinculo_display,
                "total_cursos": total,
                "concluidos": concluido,
                "progresso": round(progresso, 1)
            })

        return team_progress
