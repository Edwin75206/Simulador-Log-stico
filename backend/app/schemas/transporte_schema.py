from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


TipoTransporte = Literal["terrestre", "ferroviario", "aereo", "maritimo"]


class TransporteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    tipo: TipoTransporte
    costo_km: float = Field(..., gt=0)
    velocidad_promedio: float = Field(..., gt=0)
    capacidad_kg: float = Field(..., gt=0)
    seguridad: int = Field(..., ge=1, le=5)
    mantenimiento: float = Field(0, ge=0)
    costo_operativo: float = Field(0, ge=0)
    consumo_por_km: float = Field(0, ge=0)
    activo: bool = True


class TransporteCreate(TransporteBase):
    pass


class TransporteUpdate(TransporteBase):
    pass


class TransporteOut(TransporteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
