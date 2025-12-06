from pydantic import BaseModel

# --- Pydantic Schemas for Cursos ---

class CursoBase(BaseModel):
    titulo: str
    certificadora: str | None = None
    carga_horaria: int | None = None
    link: str | None = None
    tema: str | None = None # Corresponds to eixos_tematicos
    ano_gd: str | None = None
    lotacao_id: str | None = None
    atribuir_a_todos: bool = False
    
    conteudista: str | None = None
    disponibilidade_dias: int | None = None
    tipo_oferta: str | None = None
    apresentacao: str | None = None # Use str, Text type is SQLAlchemy specific
    publico_alvo: str | None = None
    conteudo_programatico: str | None = None
    data_lancamento: str | None = None # Using str for flexibility
    acessibilidade: str | None = None
    observacao: str | None = None

class CursoCreate(CursoBase):
    lotacao_id: str | None = None

class CursoResponse(CursoBase):
    id: str

    class Config:
        from_attributes = True
