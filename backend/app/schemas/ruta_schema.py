from datetime import datetime

from pydantic import BaseModel, Field


class RutaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    origen: str = Field(..., min_length=2, max_length=100)
    destino: str = Field(..., min_length=2, max_length=100)
    distancia_km: float = Field(..., gt=0)
    casetas: float = Field(0, ge=0)
    trafico: int = Field(..., ge=1, le=5)
    riesgo: int = Field(..., ge=1, le=5)
    estado_carretera: int = Field(..., ge=1, le=5)
    inseguridad: int = Field(..., ge=1, le=5)
    activa: bool = True


class RutaCreate(RutaBase):
    pass


class RutaUpdate(RutaBase):
    pass


class RutaOut(RutaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
