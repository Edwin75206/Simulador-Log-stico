from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.resultado_simulacion import ResultadoSimulacion
from app.models.ruta import Ruta
from app.models.simulacion import Simulacion
from app.models.transporte import Transporte
from app.schemas.resultado_schema import ResultadoOut
from app.schemas.simulacion_schema import SimulacionCreate, SimulacionDetalleOut, SimulacionOut
from app.services.calculo_logistico import calcular_resultados

router = APIRouter(prefix="/simulaciones", tags=["Simulaciones"])


@router.post("", response_model=SimulacionDetalleOut, status_code=status.HTTP_201_CREATED)
def crear_simulacion(payload: SimulacionCreate, db: Session = Depends(get_db)):
    rutas = (
        db.query(Ruta)
        .filter(
            Ruta.activa.is_(True),
            or_(
                and_(Ruta.origen == payload.origen, Ruta.destino == payload.destino),
                and_(Ruta.origen == payload.destino, Ruta.destino == payload.origen),
            ),
        )
        .all()
    )
    if not rutas:
        raise HTTPException(
            status_code=400,
            detail="No hay rutas activas para el origen y destino indicados",
        )

    transportes = (
        db.query(Transporte)
        .filter(Transporte.activo.is_(True), Transporte.capacidad_kg >= payload.peso_kg)
        .all()
    )
    if not transportes:
        raise HTTPException(
            status_code=400,
            detail="No hay transportes activos con capacidad suficiente",
        )

    simulacion = Simulacion(**payload.model_dump())
    db.add(simulacion)
    db.flush()

    resultados_calculados = calcular_resultados(rutas, transportes, payload.prioridad)
    for resultado_data in resultados_calculados:
        db.add(ResultadoSimulacion(simulacion_id=simulacion.id, **resultado_data))

    db.commit()
    return obtener_simulacion(simulacion.id, db)


@router.get("", response_model=list[SimulacionOut])
def listar_simulaciones(db: Session = Depends(get_db)):
    return db.query(Simulacion).order_by(Simulacion.id.desc()).all()


@router.get("/{simulacion_id}", response_model=SimulacionDetalleOut)
def obtener_simulacion(simulacion_id: int, db: Session = Depends(get_db)):
    simulacion = (
        db.query(Simulacion)
        .options(
            joinedload(Simulacion.resultados).joinedload(ResultadoSimulacion.ruta),
            joinedload(Simulacion.resultados).joinedload(ResultadoSimulacion.transporte),
        )
        .filter(Simulacion.id == simulacion_id)
        .first()
    )
    if not simulacion:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")
    simulacion.resultados.sort(key=lambda resultado: resultado.puntaje_total)
    return simulacion


@router.get("/{simulacion_id}/resultados", response_model=list[ResultadoOut])
def listar_resultados(simulacion_id: int, db: Session = Depends(get_db)):
    existe = db.get(Simulacion, simulacion_id)
    if not existe:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")

    return (
        db.query(ResultadoSimulacion)
        .options(
            joinedload(ResultadoSimulacion.ruta),
            joinedload(ResultadoSimulacion.transporte),
        )
        .filter(ResultadoSimulacion.simulacion_id == simulacion_id)
        .order_by(ResultadoSimulacion.recomendado.desc(), ResultadoSimulacion.puntaje_total.asc())
        .all()
    )
