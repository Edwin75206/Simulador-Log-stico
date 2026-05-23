from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


TipoTransporte = Literal["terrestre", "ferroviario", "aereo", "maritimo"]
TipoMercanciaTransporte = Literal["perecedera", "no_perecedera", "mixta"]
Combustible = Literal["gasolina", "diesel", "turbosina", "combustoleo", "electrico", "mixto"]


class TransporteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    tipo: TipoTransporte
    categoria: Optional[TipoTransporte] = None
    subcategoria: Optional[str] = Field(None, max_length=80)
    tipo_mercancia: Optional[TipoMercanciaTransporte] = None
    refrigerado: Optional[bool] = False
    combustible: Optional[Combustible] = None
    costo_km: float = Field(..., gt=0)
    velocidad_promedio: float = Field(..., gt=0)
    capacidad_kg: float = Field(..., gt=0)
    seguridad: int = Field(..., ge=1, le=5)
    mantenimiento: float = Field(0, ge=0)
    costo_operativo: float = Field(0, ge=0)
    consumo_por_km: float = Field(0, ge=0)
    rendimiento_km_litro: Optional[float] = Field(None, gt=0)
    factor_caseta: Optional[float] = Field(None, ge=0)
    costo_combustible_litro: Optional[float] = Field(None, ge=0)
    descripcion: Optional[str] = None
    uso_recomendado: Optional[str] = None
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
