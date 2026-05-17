from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.resultado_schema import ResultadoOut


Prioridad = Literal["costo", "tiempo", "seguridad", "recursos", "equilibrada"]


class SimulacionCreate(BaseModel):
    origen: str = Field(..., min_length=2, max_length=100)
    destino: str = Field(..., min_length=2, max_length=100)
    peso_kg: float = Field(..., gt=0)
    tipo_mercancia: str = Field(..., min_length=2, max_length=120)
    prioridad: Prioridad = "equilibrada"
    fecha: date


class SimulacionOut(BaseModel):
    id: int
    origen: str
    destino: str
    peso_kg: float
    tipo_mercancia: str
    prioridad: str
    fecha: date
    created_at: datetime

    model_config = {"from_attributes": True}


class SimulacionDetalleOut(SimulacionOut):
    resultados: list[ResultadoOut] = []
