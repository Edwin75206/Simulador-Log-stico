from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ruta import Ruta
from app.schemas.ruta_schema import RutaCreate, RutaOut, RutaUpdate

router = APIRouter(prefix="/rutas", tags=["Rutas"])


@router.get("", response_model=list[RutaOut])
def listar_rutas(db: Session = Depends(get_db)):
    return db.query(Ruta).order_by(Ruta.id.desc()).all()


@router.get("/{ruta_id}", response_model=RutaOut)
def obtener_ruta(ruta_id: int, db: Session = Depends(get_db)):
    ruta = db.get(Ruta, ruta_id)
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return ruta


@router.post("", response_model=RutaOut, status_code=status.HTTP_201_CREATED)
def crear_ruta(payload: RutaCreate, db: Session = Depends(get_db)):
    ruta = Ruta(**payload.model_dump())
    db.add(ruta)
    db.commit()
    db.refresh(ruta)
    return ruta


@router.put("/{ruta_id}", response_model=RutaOut)
def actualizar_ruta(ruta_id: int, payload: RutaUpdate, db: Session = Depends(get_db)):
    ruta = db.get(Ruta, ruta_id)
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    for campo, valor in payload.model_dump().items():
        setattr(ruta, campo, valor)

    db.commit()
    db.refresh(ruta)
    return ruta


@router.delete("/{ruta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ruta(ruta_id: int, db: Session = Depends(get_db)):
    ruta = db.get(Ruta, ruta_id)
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    ruta.activa = False
    db.commit()
    return None
