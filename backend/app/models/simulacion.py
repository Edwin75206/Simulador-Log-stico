from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Simulacion(Base):
    __tablename__ = "simulaciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    origen: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    destino: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    peso_kg: Mapped[float] = mapped_column(Float, nullable=False)
    tipo_mercancia: Mapped[str] = mapped_column(String(120), nullable=False)
    prioridad: Mapped[str] = mapped_column(String(30), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    resultados = relationship(
        "ResultadoSimulacion",
        back_populates="simulacion",
        cascade="all, delete-orphan",
    )
