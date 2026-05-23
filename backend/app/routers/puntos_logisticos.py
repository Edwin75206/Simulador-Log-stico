from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.punto_logistico import PuntoLogistico
from app.schemas.punto_logistico_schema import (
    PuntoLogisticoCreate,
    PuntoLogisticoOut,
    PuntoLogisticoUpdate,
)

router = APIRouter(prefix="/puntos-logisticos", tags=["Puntos logisticos"])


@router.get("", response_model=list[PuntoLogisticoOut])
def listar_puntos_logisticos(db: Session = Depends(get_db)):
    return db.query(PuntoLogistico).order_by(PuntoLogistico.nombre.asc()).all()


@router.get("/{punto_id}", response_model=PuntoLogisticoOut)
def obtener_punto_logistico(punto_id: int, db: Session = Depends(get_db)):
    punto = db.get(PuntoLogistico, punto_id)
    if not punto:
        raise HTTPException(status_code=404, detail="Punto logistico no encontrado")
    return punto


@router.post("", response_model=PuntoLogisticoOut, status_code=status.HTTP_201_CREATED)
def crear_punto_logistico(payload: PuntoLogisticoCreate, db: Session = Depends(get_db)):
    punto = PuntoLogistico(**payload.model_dump())
    db.add(punto)
    db.commit()
    db.refresh(punto)
    return punto


@router.put("/{punto_id}", response_model=PuntoLogisticoOut)
def actualizar_punto_logistico(
    punto_id: int, payload: PuntoLogisticoUpdate, db: Session = Depends(get_db)
):
    punto = db.get(PuntoLogistico, punto_id)
    if not punto:
        raise HTTPException(status_code=404, detail="Punto logistico no encontrado")

    for campo, valor in payload.model_dump().items():
        setattr(punto, campo, valor)

    db.commit()
    db.refresh(punto)
    return punto


@router.delete("/{punto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_punto_logistico(punto_id: int, db: Session = Depends(get_db)):
    punto = db.get(PuntoLogistico, punto_id)
    if not punto:
        raise HTTPException(status_code=404, detail="Punto logistico no encontrado")
    punto.activo = False
    db.commit()
    return None
