from app.models.ruta import Ruta
from app.models.transporte import Transporte
from app.services.casetas_service import obtener_casetas_estimadas


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
            consumo_por_km = _resolver_consumo_por_km(transporte)
            consumo_total = ruta.distancia_km * consumo_por_km
            costo_combustible = None
            casetas_ajustadas = _calcular_casetas_ajustadas(ruta, transporte)

            if _usa_formula_combustible(transporte, consumo_por_km):
                costo_combustible = consumo_total * transporte.costo_combustible_litro
                costo_total = (
                    costo_combustible
                    + casetas_ajustadas
                    + transporte.mantenimiento
                    + transporte.costo_operativo
                )
            else:
                costo_total = (
                    (ruta.distancia_km * transporte.costo_km)
                    + casetas_ajustadas
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

            resultados.append(
                {
                    "ruta_id": ruta.id,
                    "transporte_id": transporte.id,
                    "costo_total": round(costo_total, 2),
                    "tiempo_estimado_horas": round(tiempo_estimado, 2),
                    "puntaje_riesgo": round(puntaje_riesgo, 2),
                    "consumo_total": round(consumo_total, 2),
                    "costo_combustible": (
                        round(costo_combustible, 2) if costo_combustible is not None else None
                    ),
                    "casetas_ajustadas": (
                        round(casetas_ajustadas, 2) if casetas_ajustadas is not None else None
                    ),
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


def _resolver_consumo_por_km(transporte: Transporte) -> float:
    if transporte.consumo_por_km and transporte.consumo_por_km > 0:
        return transporte.consumo_por_km
    if transporte.rendimiento_km_litro and transporte.rendimiento_km_litro > 0:
        return 1 / transporte.rendimiento_km_litro
    return 0


def _usa_formula_combustible(transporte: Transporte, consumo_por_km: float) -> bool:
    return bool(
        consumo_por_km > 0
        and transporte.costo_combustible_litro is not None
    )


def _calcular_casetas_ajustadas(ruta: Ruta, transporte: Transporte) -> float:
    if not _es_terrestre(transporte):
        return 0

    casetas_base = obtener_casetas_estimadas(
        ruta.origen,
        ruta.destino,
        ruta.distancia_km,
        transporte,
        casetas_ruta=ruta.casetas,
    )
    factor_caseta = transporte.factor_caseta
    if factor_caseta is None:
        factor_caseta = 1
    return casetas_base * factor_caseta


def _es_terrestre(transporte: Transporte) -> bool:
    categoria = (transporte.categoria or transporte.tipo or "").strip().lower()
    return categoria == "terrestre"
