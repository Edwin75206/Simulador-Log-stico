from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.database import SessionLocal
from app.models.resultado_simulacion import ResultadoSimulacion
from app.models.simulacion import Simulacion


CONFIRMACION = "BORRAR_SIMULACIONES"


def clear_simulations() -> None:
    print(
        "Este script eliminará todas las simulaciones y resultados guardados, "
        "pero conservará rutas, transportes y puntos logísticos."
    )
    confirmacion = input(f"Escribe exactamente {CONFIRMACION} para continuar: ").strip()
    if confirmacion != CONFIRMACION:
        print("Operación cancelada. No se borró ninguna simulación.")
        return

    db = SessionLocal()
    try:
        resultados_borrados = db.query(ResultadoSimulacion).delete(
            synchronize_session=False
        )
        simulaciones_borradas = db.query(Simulacion).delete(synchronize_session=False)
        db.commit()
        print(f"Resultados borrados: {resultados_borrados}")
        print(f"Simulaciones borradas: {simulaciones_borradas}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    clear_simulations()
