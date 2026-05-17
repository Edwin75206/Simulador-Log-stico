from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.database import SessionLocal
from app.models.ruta import Ruta
from app.models.transporte import Transporte


RUTAS = [
    {
        "nombre": "Ruta Puebla - CDMX Directa",
        "origen": "Puebla",
        "destino": "CDMX",
        "distancia_km": 140,
        "casetas": 350,
        "trafico": 4,
        "riesgo": 3,
        "estado_carretera": 2,
        "inseguridad": 3,
    },
    {
        "nombre": "Ruta Puebla - CDMX Alterna",
        "origen": "Puebla",
        "destino": "CDMX",
        "distancia_km": 165,
        "casetas": 420,
        "trafico": 2,
        "riesgo": 2,
        "estado_carretera": 2,
        "inseguridad": 2,
    },
    {
        "nombre": "Ruta CDMX - Queretaro",
        "origen": "CDMX",
        "destino": "Queretaro",
        "distancia_km": 220,
        "casetas": 500,
        "trafico": 3,
        "riesgo": 2,
        "estado_carretera": 2,
        "inseguridad": 2,
    },
    {
        "nombre": "Ruta CDMX - Guadalajara",
        "origen": "CDMX",
        "destino": "Guadalajara",
        "distancia_km": 550,
        "casetas": 1200,
        "trafico": 3,
        "riesgo": 3,
        "estado_carretera": 2,
        "inseguridad": 3,
    },
    {
        "nombre": "Ruta Veracruz - Puebla",
        "origen": "Veracruz",
        "destino": "Puebla",
        "distancia_km": 280,
        "casetas": 700,
        "trafico": 2,
        "riesgo": 3,
        "estado_carretera": 3,
        "inseguridad": 3,
    },
]

TRANSPORTES = [
    {
        "nombre": "Camion ligero",
        "tipo": "terrestre",
        "costo_km": 22,
        "velocidad_promedio": 75,
        "capacidad_kg": 3500,
        "seguridad": 3,
        "mantenimiento": 300,
        "costo_operativo": 500,
        "consumo_por_km": 0.20,
    },
    {
        "nombre": "Trailer",
        "tipo": "terrestre",
        "costo_km": 35,
        "velocidad_promedio": 65,
        "capacidad_kg": 18000,
        "seguridad": 3,
        "mantenimiento": 800,
        "costo_operativo": 1200,
        "consumo_por_km": 0.35,
    },
    {
        "nombre": "Tren de carga",
        "tipo": "ferroviario",
        "costo_km": 15,
        "velocidad_promedio": 60,
        "capacidad_kg": 50000,
        "seguridad": 4,
        "mantenimiento": 1000,
        "costo_operativo": 1500,
        "consumo_por_km": 0.12,
    },
    {
        "nombre": "Avion de carga",
        "tipo": "aereo",
        "costo_km": 85,
        "velocidad_promedio": 600,
        "capacidad_kg": 8000,
        "seguridad": 5,
        "mantenimiento": 2500,
        "costo_operativo": 5000,
        "consumo_por_km": 1.50,
    },
    {
        "nombre": "Barco de carga",
        "tipo": "maritimo",
        "costo_km": 10,
        "velocidad_promedio": 35,
        "capacidad_kg": 100000,
        "seguridad": 4,
        "mantenimiento": 2000,
        "costo_operativo": 3000,
        "consumo_por_km": 0.08,
    },
]


def upsert_seed() -> None:
    db = SessionLocal()
    try:
        for data in RUTAS:
            existe = db.query(Ruta).filter(Ruta.nombre == data["nombre"]).first()
            if not existe:
                db.add(Ruta(**data))

        for data in TRANSPORTES:
            existe = db.query(Transporte).filter(Transporte.nombre == data["nombre"]).first()
            if not existe:
                db.add(Transporte(**data))

        db.commit()
        print("Datos de prueba cargados correctamente.")
    finally:
        db.close()


if __name__ == "__main__":
    upsert_seed()
