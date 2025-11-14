from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
import shutil
import os
import uuid

from ..controllers import certificado_controller, atribuicao_controller
from ..auth.auth import auth_handler
from ..resources.database import get_app_db_session
from ..auth.dependencies import is_chefia
from ..models import Certificado, StatusAtribuicao

# --- Pydantic Schemas for Request/Response ---

class CertificadoBase(BaseModel):
    link: str | None = None

class CertificadoCreate(CertificadoBase):
    atribuicao_id: str

class CertificadoResponse(CertificadoBase):
    id: str
    file_path: str | None = None
    validado: bool

    class Config:
        from_attributes = True

class ValidacaoRequest(BaseModel):
    atribuicao_id: str
    status: StatusAtribuicao # Deve ser VALIDADO ou RECUSADO

# --- Router Definition ---

router = APIRouter(
    prefix="/api/certificados",
    tags=["Certificados"],
)

UPLOADS_DIR = "src/static/uploads"

@router.post("/upload", response_model=CertificadoResponse, dependencies=[Depends(auth_handler.decode_token)])
async def registrar_certificado_upload(
    atribuicao_id: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Registra um novo certificado fazendo o upload de um arquivo PDF.
    """
    # Garante que o diretório de uploads existe
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    
    # Gera um nome de arquivo único para evitar sobrescrita
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOADS_DIR, unique_filename)
    
    # Salva o arquivo
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Cria a entrada do certificado no banco
    # Obter o curso_id da atribuição
    atribuicao = await atribuicao_controller.obter_atribuicao_por_id(db, atribuicao_id)
    if not atribuicao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atribuição não encontrada")

    certificado_data = {"file_path": file_path, "curso_id": atribuicao.curso_id}
    novo_certificado = await certificado_controller.registrar_certificado(db, certificado_data)

    # Atualiza a atribuição
    await atribuicao_controller.atualizar_atribuicao_com_certificado(
        db=db,
        atribuicao_id=atribuicao_id,
        certificado_id=novo_certificado.id,
        novo_status=StatusAtribuicao.REALIZADO
    )

    return novo_certificado

@router.post("/link", response_model=CertificadoResponse, dependencies=[Depends(auth_handler.decode_token)])
async def registrar_certificado_link(
    certificado_data: CertificadoCreate,
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Registra um novo certificado a partir de um link externo.
    """
    # Cria a entrada do certificado no banco
    novo_certificado = await certificado_controller.registrar_certificado(db, {"link": certificado_data.link})

    # Atualiza a atribuição
    await atribuicao_controller.atualizar_atribuicao_com_certificado(
        db=db,
        atribuicao_id=certificado_data.atribuicao_id,
        certificado_id=novo_certificado.id,
        novo_status=StatusAtribuicao.REALIZADO
    )
    
    return novo_certificado

@router.get("/{certificado_id}", response_model=CertificadoResponse, dependencies=[Depends(auth_handler.decode_token)])
async def obter_certificado(
    certificado_id: str,
    db: AsyncSession = Depends(get_app_db_session)
):
    """Obtém um certificado pelo ID."""
    certificado = await certificado_controller.obter_certificado_por_id(db, certificado_id)
    if certificado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificado não encontrado")
    return certificado

@router.post("/validar", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth_handler.decode_token), Depends(is_chefia)])
async def validar_certificado(
    validacao: ValidacaoRequest,
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Valida ou recusa a submissão de um certificado. (Requer perfil de Chefia ou UDP)
    """
    if validacao.status not in [StatusAtribuicao.VALIDADO, StatusAtribuicao.RECUSADO]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O status de validação deve ser 'Validado' ou 'Recusado'."
        )
    
    await atribuicao_controller.validar_atribuicao(
        db=db,
        atribuicao_id=validacao.atribuicao_id,
        status=validacao.status
    )
    return
