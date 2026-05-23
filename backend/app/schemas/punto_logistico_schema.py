from datetime import datetime
from typing import Literal, Optional
from urllib.parse import quote_plus

from pydantic import BaseModel, Field, computed_field


TipoPuntoLogistico = Literal[
    "central_abasto", "puerto", "central_autobuses", "aeropuerto"
]


class PuntoLogisticoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=160)
    tipo: TipoPuntoLogistico
    ciudad: str = Field(..., min_length=2, max_length=100)
    estado: str = Field(..., min_length=2, max_length=100)
    direccion: str = Field("", max_length=255)
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    activo: bool = True


class PuntoLogisticoCreate(PuntoLogisticoBase):
    pass


class PuntoLogisticoUpdate(PuntoLogisticoBase):
    pass


class PuntoLogisticoOut(PuntoLogisticoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def google_maps_url(self) -> str:
        if self.latitud is not None and self.longitud is not None:
            query = f"{self.latitud},{self.longitud}"
        else:
            query = f"{self.nombre} {self.ciudad} {self.estado}"
        return f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}"
