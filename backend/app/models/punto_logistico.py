from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PuntoLogistico(Base):
    __tablename__ = "puntos_logisticos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    ciudad: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    latitud: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitud: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    rutas_origen = relationship(
        "Ruta", foreign_keys="Ruta.origen_id", back_populates="punto_origen"
    )
    rutas_destino = relationship(
        "Ruta", foreign_keys="Ruta.destino_id", back_populates="punto_destino"
    )
