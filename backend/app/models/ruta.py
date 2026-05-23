from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Ruta(Base):
    __tablename__ = "rutas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    origen: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    destino: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    origen_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("puntos_logisticos.id"), nullable=True
    )
    destino_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("puntos_logisticos.id"), nullable=True
    )
    distancia_km: Mapped[float] = mapped_column(Float, nullable=False)
    casetas: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    trafico: Mapped[int] = mapped_column(Integer, nullable=False)
    riesgo: Mapped[int] = mapped_column(Integer, nullable=False)
    estado_carretera: Mapped[int] = mapped_column(Integer, nullable=False)
    inseguridad: Mapped[int] = mapped_column(Integer, nullable=False)
    activa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    resultados = relationship("ResultadoSimulacion", back_populates="ruta")
    punto_origen = relationship(
        "PuntoLogistico", foreign_keys=[origen_id], back_populates="rutas_origen"
    )
    punto_destino = relationship(
        "PuntoLogistico", foreign_keys=[destino_id], back_populates="rutas_destino"
    )
