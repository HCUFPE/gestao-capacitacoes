from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from uuid import uuid4

from ..models import Certificado

async def listar_certificados(db: AsyncSession) -> List[Certificado]:
    """
    Lista todos os certificados usando o ORM do SQLAlchemy.
    """
    result = await db.execute(select(Certificado))
    return result.scalars().all()

async def registrar_certificado(db: AsyncSession, certificado_data: Dict[str, Any]) -> Certificado:
    """
    Registra um novo certificado usando o ORM do SQLAlchemy.
    """
    new_id = str(uuid4())
    certificado_data["id"] = new_id
    
    new_certificado = Certificado(**certificado_data)
    db.add(new_certificado)
    await db.commit()
    await db.refresh(new_certificado)
    return new_certificado

async def obter_certificado_por_id(db: AsyncSession, certificado_id: str) -> Certificado | None:
    """
    Obtém um certificado pelo ID usando o ORM do SQLAlchemy.
    """
    result = await db.execute(select(Certificado).where(Certificado.id == certificado_id))
    return result.scalars().first()