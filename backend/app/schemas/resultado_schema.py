from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.ruta_schema import RutaOut
from app.schemas.transporte_schema import TransporteOut


class ResultadoOut(BaseModel):
    id: int
    simulacion_id: int
    ruta_id: int
    transporte_id: int
    costo_total: float
    tiempo_estimado_horas: float
    puntaje_riesgo: float
    consumo_total: float
    costo_combustible: Optional[float] = None
    casetas_ajustadas: Optional[float] = None
    puntaje_total: float
    recomendado: bool
    created_at: datetime
    ruta: RutaOut
    transporte: TransporteOut

    model_config = {"from_attributes": True}
