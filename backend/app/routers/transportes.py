from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transporte import Transporte
from app.schemas.transporte_schema import TransporteCreate, TransporteOut, TransporteUpdate

router = APIRouter(prefix="/transportes", tags=["Transportes"])


@router.get("", response_model=list[TransporteOut])
def listar_transportes(db: Session = Depends(get_db)):
    return db.query(Transporte).order_by(Transporte.id.desc()).all()


@router.get("/{transporte_id}", response_model=TransporteOut)
def obtener_transporte(transporte_id: int, db: Session = Depends(get_db)):
    transporte = db.get(Transporte, transporte_id)
    if not transporte:
        raise HTTPException(status_code=404, detail="Transporte no encontrado")
    return transporte


@router.post("", response_model=TransporteOut, status_code=status.HTTP_201_CREATED)
def crear_transporte(payload: TransporteCreate, db: Session = Depends(get_db)):
    data = _normalizar_payload(payload.model_dump())
    transporte = Transporte(**data)
    db.add(transporte)
    db.commit()
    db.refresh(transporte)
    return transporte


@router.put("/{transporte_id}", response_model=TransporteOut)
def actualizar_transporte(
    transporte_id: int, payload: TransporteUpdate, db: Session = Depends(get_db)
):
    transporte = db.get(Transporte, transporte_id)
    if not transporte:
        raise HTTPException(status_code=404, detail="Transporte no encontrado")

    for campo, valor in _normalizar_payload(payload.model_dump()).items():
        setattr(transporte, campo, valor)

    db.commit()
    db.refresh(transporte)
    return transporte


@router.delete("/{transporte_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_transporte(transporte_id: int, db: Session = Depends(get_db)):
    transporte = db.get(Transporte, transporte_id)
    if not transporte:
        raise HTTPException(status_code=404, detail="Transporte no encontrado")
    transporte.activo = False
    db.commit()
    return None


def _normalizar_payload(data: dict) -> dict:
    if data.get("categoria"):
        data["tipo"] = data["categoria"]
    if data.get("rendimiento_km_litro") and data["rendimiento_km_litro"] > 0:
        data["consumo_por_km"] = round(1 / data["rendimiento_km_litro"], 4)
    return data
