from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Transporte(Base):
    __tablename__ = "transportes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    costo_km: Mapped[float] = mapped_column(Float, nullable=False)
    velocidad_promedio: Mapped[float] = mapped_column(Float, nullable=False)
    capacidad_kg: Mapped[float] = mapped_column(Float, nullable=False)
    seguridad: Mapped[int] = mapped_column(Integer, nullable=False)
    mantenimiento: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    costo_operativo: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    consumo_por_km: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    resultados = relationship("ResultadoSimulacion", back_populates="transporte")
