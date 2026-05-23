from typing import Optional


def obtener_casetas_estimadas(
    origen: str,
    destino: str,
    distancia_km: float,
    transporte,
    *,
    casetas_ruta: Optional[float] = None,
) -> float:
    """Return the route's base toll estimate before transport size factors."""
    if casetas_ruta is not None and casetas_ruta > 0:
        return casetas_ruta

    # The external provider hook is intentionally not called yet. This local
    # path keeps academic simulations deterministic and offline.
    _ = (origen, destino, transporte)
    return calcular_casetas_base_academicas(distancia_km)


def _obtener_casetas_desde_fuente_externa_opcional(
    origen: str,
    destino: str,
    distancia_km: float,
    transporte,
) -> Optional[float]:
    # Future opt-in provider hook. Google Routes API exposes TollInfo and
    # estimatedPrice but needs Routes API billing and credentials. SICT/Mappir
    # can expose toll information in Mexico, but the simulator should not depend
    # on brittle page scraping if a stable public API is unavailable. INEGI Ruteo
    # is another possible provider; tariff updates can lag real toll changes.
    _ = (origen, destino, distancia_km, transporte)
    return None


def calcular_casetas_base_academicas(distancia_km: Optional[float]) -> float:
    if distancia_km is None or distancia_km <= 0:
        return 0

    if distancia_km < 80:
        casetas = 80
    elif distancia_km <= 200:
        casetas = distancia_km * 2.2
    elif distancia_km <= 500:
        casetas = distancia_km * 2.8
    else:
        casetas = distancia_km * 3.2

    return round(casetas / 10) * 10
