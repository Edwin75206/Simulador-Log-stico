from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ResultadoSimulacion(Base):
    __tablename__ = "resultados_simulacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    simulacion_id: Mapped[int] = mapped_column(ForeignKey("simulaciones.id"), nullable=False)
    ruta_id: Mapped[int] = mapped_column(ForeignKey("rutas.id"), nullable=False)
    transporte_id: Mapped[int] = mapped_column(ForeignKey("transportes.id"), nullable=False)
    costo_total: Mapped[float] = mapped_column(Float, nullable=False)
    tiempo_estimado_horas: Mapped[float] = mapped_column(Float, nullable=False)
    puntaje_riesgo: Mapped[float] = mapped_column(Float, nullable=False)
    consumo_total: Mapped[float] = mapped_column(Float, nullable=False)
    costo_combustible: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    casetas_ajustadas: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    puntaje_total: Mapped[float] = mapped_column(Float, nullable=False)
    recomendado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    simulacion = relationship("Simulacion", back_populates="resultados")
    ruta = relationship("Ruta", back_populates="resultados")
    transporte = relationship("Transporte", back_populates="resultados")
