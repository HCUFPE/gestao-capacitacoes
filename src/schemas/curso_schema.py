from pydantic import BaseModel

# --- Pydantic Schemas for Cursos ---

class CursoBase(BaseModel):
    titulo: str
    certificadora: str | None = None
    carga_horaria: int | None = None
    link: str | None = None
    ano_gd: str | None = None
    lotacao_id: str | None = None
    atribuir_a_todos: bool = False

class CursoCreate(CursoBase):
    lotacao_id: str | None = None

class CursoResponse(CursoBase):
    id: str

    class Config:
        from_attributes = True
