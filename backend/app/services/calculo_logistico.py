from app.models.ruta import Ruta
from app.models.transporte import Transporte


FACTORES_TRAFICO = {
    1: 1.05,
    2: 1.15,
    3: 1.30,
    4: 1.45,
    5: 1.60,
}


def _normalizar(valor: float, minimo: float, maximo: float) -> float:
    if maximo == minimo:
        return 0
    return (valor - minimo) / (maximo - minimo)


def calcular_resultados(rutas: list[Ruta], transportes: list[Transporte], prioridad: str) -> list[dict]:
    resultados = []

    for ruta in rutas:
        for transporte in transportes:
            costo_total = (
                (ruta.distancia_km * transporte.costo_km)
                + ruta.casetas
                + transporte.mantenimiento
                + transporte.costo_operativo
            )
            tiempo_base = ruta.distancia_km / transporte.velocidad_promedio
            tiempo_estimado = tiempo_base * FACTORES_TRAFICO[ruta.trafico]
            riesgo_ruta = (
                ruta.riesgo + ruta.trafico + ruta.estado_carretera + ruta.inseguridad
            ) / 4
            riesgo_transporte = 6 - transporte.seguridad
            puntaje_riesgo = (riesgo_ruta + riesgo_transporte) / 2
            consumo_total = ruta.distancia_km * transporte.consumo_por_km

            resultados.append(
                {
                    "ruta_id": ruta.id,
                    "transporte_id": transporte.id,
                    "costo_total": round(costo_total, 2),
                    "tiempo_estimado_horas": round(tiempo_estimado, 2),
                    "puntaje_riesgo": round(puntaje_riesgo, 2),
                    "consumo_total": round(consumo_total, 2),
                    "puntaje_total": 0,
                    "recomendado": False,
                }
            )

    if not resultados:
        return resultados

    _aplicar_puntaje_equilibrado(resultados)
    indice_recomendado = _seleccionar_recomendado(resultados, prioridad)
    resultados[indice_recomendado]["recomendado"] = True
    return resultados


def _aplicar_puntaje_equilibrado(resultados: list[dict]) -> None:
    campos = {
        "costo_total": [r["costo_total"] for r in resultados],
        "tiempo_estimado_horas": [r["tiempo_estimado_horas"] for r in resultados],
        "puntaje_riesgo": [r["puntaje_riesgo"] for r in resultados],
        "consumo_total": [r["consumo_total"] for r in resultados],
    }

    for resultado in resultados:
        costo_norm = _normalizar(
            resultado["costo_total"], min(campos["costo_total"]), max(campos["costo_total"])
        )
        tiempo_norm = _normalizar(
            resultado["tiempo_estimado_horas"],
            min(campos["tiempo_estimado_horas"]),
            max(campos["tiempo_estimado_horas"]),
        )
        riesgo_norm = _normalizar(
            resultado["puntaje_riesgo"],
            min(campos["puntaje_riesgo"]),
            max(campos["puntaje_riesgo"]),
        )
        consumo_norm = _normalizar(
            resultado["consumo_total"],
            min(campos["consumo_total"]),
            max(campos["consumo_total"]),
        )
        resultado["puntaje_total"] = round(
            (costo_norm * 0.35)
            + (tiempo_norm * 0.30)
            + (riesgo_norm * 0.25)
            + (consumo_norm * 0.10),
            4,
        )


def _seleccionar_recomendado(resultados: list[dict], prioridad: str) -> int:
    criterio = {
        "costo": "costo_total",
        "tiempo": "tiempo_estimado_horas",
        "seguridad": "puntaje_riesgo",
        "recursos": "consumo_total",
        "equilibrada": "puntaje_total",
    }[prioridad]

    return min(range(len(resultados)), key=lambda i: resultados[i][criterio])
