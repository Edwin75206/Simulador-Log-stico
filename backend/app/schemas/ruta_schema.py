from datetime import datetime
from typing import Optional
from urllib.parse import quote_plus

from pydantic import BaseModel, Field, computed_field

from app.schemas.punto_logistico_schema import PuntoLogisticoOut


class RutaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    origen: str = Field(..., min_length=2, max_length=100)
    destino: str = Field(..., min_length=2, max_length=100)
    origen_id: Optional[int] = None
    destino_id: Optional[int] = None
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
    punto_origen: Optional[PuntoLogisticoOut] = None
    punto_destino: Optional[PuntoLogisticoOut] = None

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def google_maps_url(self) -> str:
        origin = _maps_value(self.punto_origen, self.origen)
        destination = _maps_value(self.punto_destino, self.destino)
        return (
            "https://www.google.com/maps/dir/?api=1"
            f"&origin={quote_plus(origin)}"
            f"&destination={quote_plus(destination)}"
            "&travelmode=driving"
        )


def _maps_value(punto: Optional[PuntoLogisticoOut], texto: str) -> str:
    if punto and punto.latitud is not None and punto.longitud is not None:
        return f"{punto.latitud},{punto.longitud}"
    if punto:
        return f"{punto.nombre} {punto.ciudad} {punto.estado}"
    return texto
