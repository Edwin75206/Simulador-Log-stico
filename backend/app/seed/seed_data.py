from pathlib import Path
from itertools import combinations
from math import asin, cos, radians, sin, sqrt
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.database import SessionLocal
from app.models.punto_logistico import PuntoLogistico
from app.models.ruta import Ruta
from app.models.transporte import Transporte
from app.services.casetas_service import calcular_casetas_base_academicas


PUNTOS_LOGISTICOS = [
    {
        "nombre": "Central de Abasto CDMX",
        "tipo": "central_abasto",
        "ciudad": "Ciudad de México",
        "estado": "Ciudad de México",
        "direccion": "Iztapalapa, Ciudad de México",
    },
    {
        "nombre": "Mercado de Abastos Guadalajara",
        "tipo": "central_abasto",
        "ciudad": "Guadalajara",
        "estado": "Jalisco",
        "direccion": "Zona del Mercado de Abastos, Guadalajara",
    },
    {
        "nombre": "Central de Abasto Monterrey",
        "tipo": "central_abasto",
        "ciudad": "Monterrey",
        "estado": "Nuevo León",
        "direccion": "Área metropolitana de Monterrey",
    },
    {
        "nombre": "Central de Abasto Puebla",
        "tipo": "central_abasto",
        "ciudad": "Puebla",
        "estado": "Puebla",
        "direccion": "Puebla, Puebla",
    },
    {
        "nombre": "Central de Abasto Toluca",
        "tipo": "central_abasto",
        "ciudad": "Toluca",
        "estado": "Estado de México",
        "direccion": "Toluca, Estado de México",
    },
    {
        "nombre": "Central de Abasto León",
        "tipo": "central_abasto",
        "ciudad": "León",
        "estado": "Guanajuato",
        "direccion": "León, Guanajuato",
    },
    {
        "nombre": "Puerto de Manzanillo",
        "tipo": "puerto",
        "ciudad": "Manzanillo",
        "estado": "Colima",
        "direccion": "Puerto de Manzanillo, Colima",
    },
    {
        "nombre": "Puerto de Veracruz",
        "tipo": "puerto",
        "ciudad": "Veracruz",
        "estado": "Veracruz",
        "direccion": "Puerto de Veracruz, Veracruz",
    },
    {
        "nombre": "Puerto de Lázaro Cárdenas",
        "tipo": "puerto",
        "ciudad": "Lázaro Cárdenas",
        "estado": "Michoacán",
        "direccion": "Puerto de Lázaro Cárdenas, Michoacán",
    },
    {
        "nombre": "Puerto de Altamira",
        "tipo": "puerto",
        "ciudad": "Altamira",
        "estado": "Tamaulipas",
        "direccion": "Puerto de Altamira, Tamaulipas",
    },
    {
        "nombre": "Puerto de Ensenada",
        "tipo": "puerto",
        "ciudad": "Ensenada",
        "estado": "Baja California",
        "direccion": "Puerto de Ensenada, Baja California",
    },
    {
        "nombre": "Puerto de Progreso",
        "tipo": "puerto",
        "ciudad": "Progreso",
        "estado": "Yucatán",
        "direccion": "Puerto de Progreso, Yucatán",
    },
    {
        "nombre": "TAPO",
        "tipo": "central_autobuses",
        "ciudad": "Ciudad de México",
        "estado": "Ciudad de México",
        "direccion": "Terminal de Autobuses de Pasajeros de Oriente, Ciudad de México",
    },
    {
        "nombre": "Central del Norte CDMX",
        "tipo": "central_autobuses",
        "ciudad": "Ciudad de México",
        "estado": "Ciudad de México",
        "direccion": "Terminal Central del Norte, Ciudad de México",
    },
    {
        "nombre": "Central de Autobuses Observatorio",
        "tipo": "central_autobuses",
        "ciudad": "Ciudad de México",
        "estado": "Ciudad de México",
        "direccion": "Observatorio, Ciudad de México",
    },
    {
        "nombre": "Central de Autobuses del Sur Taxqueña",
        "tipo": "central_autobuses",
        "ciudad": "Ciudad de México",
        "estado": "Ciudad de México",
        "direccion": "Taxqueña, Ciudad de México",
    },
    {
        "nombre": "Central de Autobuses Monterrey",
        "tipo": "central_autobuses",
        "ciudad": "Monterrey",
        "estado": "Nuevo León",
        "direccion": "Monterrey, Nuevo León",
    },
    {
        "nombre": "CAPU Puebla",
        "tipo": "central_autobuses",
        "ciudad": "Puebla",
        "estado": "Puebla",
        "direccion": "Central de Autobuses de Puebla",
    },
    {
        "nombre": "Aeropuerto Internacional de la Ciudad de México",
        "tipo": "aeropuerto",
        "ciudad": "Ciudad de México",
        "estado": "Ciudad de México",
        "direccion": "AICM, Ciudad de México",
    },
    {
        "nombre": "Aeropuerto Internacional Felipe Ángeles",
        "tipo": "aeropuerto",
        "ciudad": "Zumpango",
        "estado": "Estado de México",
        "direccion": "AIFA, Zumpango, Estado de México",
    },
    {
        "nombre": "Aeropuerto Internacional de Cancún",
        "tipo": "aeropuerto",
        "ciudad": "Cancún",
        "estado": "Quintana Roo",
        "direccion": "Cancún, Quintana Roo",
    },
    {
        "nombre": "Aeropuerto Internacional de Guadalajara",
        "tipo": "aeropuerto",
        "ciudad": "Guadalajara",
        "estado": "Jalisco",
        "direccion": "Tlajomulco de Zúñiga, Jalisco",
    },
    {
        "nombre": "Aeropuerto Internacional de Monterrey",
        "tipo": "aeropuerto",
        "ciudad": "Monterrey",
        "estado": "Nuevo León",
        "direccion": "Apodaca, Nuevo León",
    },
    {
        "nombre": "Aeropuerto Internacional de Tijuana",
        "tipo": "aeropuerto",
        "ciudad": "Tijuana",
        "estado": "Baja California",
        "direccion": "Tijuana, Baja California",
    },
]

COORDENADAS_PUNTOS = {
    "Central de Abasto CDMX": (19.3733, -99.0889),
    "Mercado de Abastos Guadalajara": (20.6547, -103.3802),
    "Central de Abasto Monterrey": (25.7171, -100.2366),
    "Central de Abasto Puebla": (19.0706, -98.1729),
    "Central de Abasto Toluca": (19.3048, -99.6367),
    "Central de Abasto León": (21.0987, -101.6419),
    "Puerto de Manzanillo": (19.0631, -104.3084),
    "Puerto de Veracruz": (19.2001, -96.1332),
    "Puerto de Lázaro Cárdenas": (17.9583, -102.1942),
    "Puerto de Altamira": (22.4881, -97.8588),
    "Puerto de Ensenada": (31.8563, -116.6256),
    "Puerto de Progreso": (21.2812, -89.6636),
    "TAPO": (19.4303, -99.1121),
    "Central del Norte CDMX": (19.4790, -99.1405),
    "Central de Autobuses Observatorio": (19.3985, -99.2008),
    "Central de Autobuses del Sur Taxqueña": (19.3396, -99.1233),
    "Central de Autobuses Monterrey": (25.6850, -100.3190),
    "CAPU Puebla": (19.0752, -98.2076),
    "Aeropuerto Internacional de la Ciudad de México": (19.4361, -99.0719),
    "Aeropuerto Internacional Felipe Ángeles": (19.7374, -99.0250),
    "Aeropuerto Internacional de Cancún": (21.0413, -86.8746),
    "Aeropuerto Internacional de Guadalajara": (20.5218, -103.3112),
    "Aeropuerto Internacional de Monterrey": (25.7785, -100.1069),
    "Aeropuerto Internacional de Tijuana": (32.5411, -116.9702),
}


RUTAS_LEGADO = [
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


RUTAS_LOGISTICAS = [
    ("Central de Abasto CDMX", "Central de Abasto Puebla", 135, 360, 4, 3, 2, 3),
    ("Central de Abasto CDMX", "Mercado de Abastos Guadalajara", 545, 1250, 3, 3, 2, 3),
    ("Central de Abasto Monterrey", "Central de Abasto León", 690, 1450, 3, 3, 2, 3),
    ("Central de Abasto Puebla", "Puerto de Veracruz", 280, 700, 2, 3, 3, 3),
    (
        "CAPU Puebla",
        "TAPO",
        135,
        340,
        4,
        3,
        2,
        3,
    ),
    ("Central del Norte CDMX", "Central de Autobuses Monterrey", 910, 1850, 3, 3, 2, 3),
    ("Puerto de Veracruz", "Puerto de Altamira", 470, 950, 2, 3, 2, 3),
    ("Puerto de Manzanillo", "Puerto de Lázaro Cárdenas", 335, 700, 2, 3, 2, 3),
    ("Puerto de Ensenada", "Puerto de Manzanillo", 2200, 4200, 3, 3, 3, 3),
    ("Puerto de Progreso", "Puerto de Veracruz", 1000, 1800, 2, 3, 3, 3),
    (
        "Aeropuerto Internacional de la Ciudad de México",
        "Aeropuerto Internacional de Cancún",
        1620,
        0,
        1,
        2,
        1,
        2,
    ),
    (
        "Aeropuerto Internacional de la Ciudad de México",
        "Aeropuerto Internacional de Guadalajara",
        460,
        0,
        1,
        2,
        1,
        2,
    ),
    (
        "Aeropuerto Internacional Felipe Ángeles",
        "Aeropuerto Internacional de Monterrey",
        720,
        0,
        1,
        2,
        1,
        2,
    ),
    (
        "Aeropuerto Internacional de Guadalajara",
        "Aeropuerto Internacional de Tijuana",
        1900,
        0,
        1,
        2,
        1,
        2,
    ),
    ("Central de Abasto CDMX", "Puerto de Veracruz", 400, 900, 3, 3, 2, 3),
    ("Mercado de Abastos Guadalajara", "Puerto de Manzanillo", 300, 650, 3, 3, 2, 3),
    ("Central de Abasto Monterrey", "Puerto de Altamira", 520, 1100, 2, 3, 2, 3),
    (
        "Central de Abasto CDMX",
        "Aeropuerto Internacional de la Ciudad de México",
        12,
        0,
        5,
        3,
        3,
        3,
    ),
    ("Central de Abasto Puebla", "Aeropuerto Internacional Felipe Ángeles", 150, 420, 3, 3, 2, 3),
]


TRANSPORTES = []


def _transporte(
    nombre,
    categoria,
    subcategoria,
    tipo_mercancia,
    refrigerado,
    combustible,
    rendimiento,
    factor_caseta,
    costo_combustible_litro,
    capacidad_kg,
    velocidad_promedio,
    mantenimiento,
    costo_operativo,
    seguridad,
    uso_recomendado,
    descripcion="Dato académico simulado para comparación logística.",
):
    return {
        "nombre": nombre,
        "tipo": categoria,
        "categoria": categoria,
        "subcategoria": subcategoria,
        "tipo_mercancia": tipo_mercancia,
        "refrigerado": refrigerado,
        "combustible": combustible,
        "rendimiento_km_litro": rendimiento,
        "consumo_por_km": round(1 / rendimiento, 4),
        "factor_caseta": factor_caseta,
        "costo_combustible_litro": costo_combustible_litro,
        "capacidad_kg": capacidad_kg,
        "velocidad_promedio": velocidad_promedio,
        "costo_km": round(costo_combustible_litro / rendimiento, 2),
        "mantenimiento": mantenimiento,
        "costo_operativo": costo_operativo,
        "seguridad": seguridad,
        "descripcion": descripcion,
        "uso_recomendado": uso_recomendado,
        "activo": True,
    }


TRANSPORTES.extend(
    [
        _transporte("Camioneta de carga ligera", "terrestre", "camioneta_carga", "no_perecedera", False, "gasolina", 9, 0.7, 24, 1000, 80, 250, 450, 3, "entregas urbanas y paquetería ligera"),
        _transporte("Camioneta refrigerada", "terrestre", "camioneta_refrigerada", "perecedera", True, "diesel", 7, 0.8, 25, 1200, 75, 400, 650, 4, "alimentos, medicamentos y productos perecederos"),
        _transporte("Camión rabón seco", "terrestre", "camion_rabon", "no_perecedera", False, "diesel", 5, 1.0, 25, 7000, 70, 700, 1000, 3, "carga seca regional"),
        _transporte("Camión rabón refrigerado", "terrestre", "camion_rabon_refrigerado", "perecedera", True, "diesel", 4.5, 1.1, 25, 6500, 68, 900, 1200, 4, "productos frescos y congelados"),
        _transporte("Torton seco", "terrestre", "torton", "no_perecedera", False, "diesel", 3.8, 1.3, 25, 14000, 65, 1100, 1600, 3, "carga mediana de larga distancia"),
        _transporte("Torton refrigerado", "terrestre", "torton_refrigerado", "perecedera", True, "diesel", 3.4, 1.4, 25, 13000, 62, 1350, 1900, 4, "alimentos perecederos en volumen medio"),
        _transporte("Tráiler caja seca", "terrestre", "trailer_sencillo", "no_perecedera", False, "diesel", 2.8, 1.6, 25, 28000, 62, 1800, 2600, 3, "carga seca nacional"),
        _transporte("Tráiler refrigerado", "terrestre", "trailer_refrigerado", "perecedera", True, "diesel", 2.5, 1.7, 25, 26000, 60, 2200, 3100, 4, "productos congelados o refrigerados"),
        _transporte("Full tráiler caja seca", "terrestre", "full_trailer", "no_perecedera", False, "diesel", 2.0, 2.0, 25, 50000, 55, 3000, 4200, 3, "carga masiva no perecedera"),
        _transporte("Full tráiler refrigerado", "terrestre", "full_trailer_refrigerado", "perecedera", True, "diesel", 1.8, 2.1, 25, 46000, 52, 3600, 5000, 4, "carga masiva perecedera"),
        _transporte("Tren de carga general GE ES44AC", "ferroviario", "tren_carga_general_ge_es44ac", "mixta", False, "diesel", 14, 0, 25, 80000, 60, 5000, 7000, 4, "carga masiva terrestre en corredores ferroviarios"),
        _transporte("Tren intermodal doble estiba", "ferroviario", "tren_intermodal_doble_estiba", "mixta", False, "diesel", 13, 0, 25, 120000, 65, 6500, 9000, 4, "contenedores y carga intermodal de larga distancia"),
        _transporte("Tren refrigerado multimodal", "ferroviario", "tren_refrigerado_multimodal", "perecedera", True, "diesel", 11, 0, 25, 70000, 58, 8000, 11000, 4, "perecederos refrigerados en corredores ferroviarios"),
        _transporte("Tren granelero tolvas", "ferroviario", "tren_granelero_tolvas", "no_perecedera", False, "diesel", 15, 0, 25, 150000, 55, 7000, 9500, 3, "granos, minerales y materiales a granel"),
        _transporte("Tren automotriz madrina ferroviaria", "ferroviario", "tren_automotriz_madrina", "no_perecedera", False, "diesel", 12, 0, 25, 90000, 62, 7500, 10500, 4, "vehículos, autopartes y carga especializada"),
    ]
)

TRANSPORTES.extend(
    [
        _transporte("Avión ligero de carga", "aereo", "avion_ligero_carga", "mixta", False, "turbosina", 1.2, 0, 28, 2000, 350, 5000, 9000, 5, "paquetería urgente de bajo volumen"),
        _transporte("Avión regional de carga", "aereo", "avion_regional_carga", "mixta", True, "turbosina", 0.9, 0, 28, 6000, 450, 9000, 15000, 5, "carga regional sensible al tiempo"),
        _transporte("Avión turbohélice carguero", "aereo", "turbohelice_carguero", "mixta", True, "turbosina", 0.75, 0, 28, 9000, 500, 12000, 18000, 5, "mercancía regional y perecedera ligera"),
        _transporte("Boeing 737 carguero", "aereo", "boeing_737_carguero", "mixta", False, "turbosina", 0.45, 0, 28, 20000, 780, 24000, 35000, 5, "carga aérea nacional"),
        _transporte("Boeing 757 carguero", "aereo", "boeing_757_carguero", "mixta", True, "turbosina", 0.35, 0, 28, 35000, 820, 30000, 46000, 5, "carga aérea de medio alcance"),
        _transporte("Boeing 767 carguero", "aereo", "boeing_767_carguero", "mixta", True, "turbosina", 0.28, 0, 28, 52000, 850, 38000, 60000, 5, "carga aérea internacional"),
        _transporte("Airbus A330 carguero", "aereo", "airbus_a330_carguero", "mixta", True, "turbosina", 0.24, 0, 28, 65000, 860, 45000, 72000, 5, "carga aérea internacional de alto volumen"),
        _transporte("Boeing 777 carguero", "aereo", "boeing_777_carguero", "mixta", True, "turbosina", 0.18, 0, 28, 100000, 890, 62000, 95000, 5, "carga aérea pesada de largo alcance"),
        _transporte("Boeing 747 carguero", "aereo", "boeing_747_carguero", "mixta", True, "turbosina", 0.15, 0, 28, 120000, 900, 80000, 120000, 5, "carga aérea masiva intercontinental"),
        _transporte("Antonov carga sobredimensionada", "aereo", "antonov_carga_sobredimensionada", "mixta", False, "turbosina", 0.10, 0, 28, 120000, 760, 120000, 180000, 4, "carga sobredimensionada y proyectos especiales"),
    ]
)

TRANSPORTES.extend(
    [
        _transporte("Lancha de carga costera", "maritimo", "lancha_carga_costera", "no_perecedera", False, "diesel", 0.8, 0, 25, 15000, 35, 2500, 5000, 3, "carga costera ligera"),
        _transporte("Barcaza de carga", "maritimo", "barcaza_carga", "no_perecedera", False, "diesel", 0.5, 0, 25, 80000, 25, 5000, 9000, 3, "traslado fluvial o portuario"),
        _transporte("Buque feeder", "maritimo", "buque_feeder", "mixta", False, "combustoleo", 0.18, 0, 18, 5000000, 35, 30000, 70000, 4, "alimentación de puertos regionales"),
        _transporte("Buque portacontenedores pequeño", "maritimo", "buque_portacontenedores_pequeno", "mixta", False, "combustoleo", 0.12, 0, 18, 12000000, 38, 50000, 100000, 4, "contenedores en rutas regionales"),
        _transporte("Buque portacontenedores mediano", "maritimo", "buque_portacontenedores_mediano", "mixta", False, "combustoleo", 0.09, 0, 18, 30000000, 40, 90000, 160000, 4, "contenedores en rutas internacionales"),
        _transporte("Buque portacontenedores grande", "maritimo", "buque_portacontenedores_grande", "mixta", False, "combustoleo", 0.06, 0, 18, 70000000, 42, 150000, 260000, 4, "carga contenerizada masiva"),
        _transporte("Buque refrigerado", "maritimo", "buque_refrigerado", "perecedera", True, "combustoleo", 0.07, 0, 18, 25000000, 38, 130000, 240000, 4, "frutas, alimentos congelados y perecederos"),
        _transporte("Buque granelero", "maritimo", "buque_granelero", "no_perecedera", False, "combustoleo", 0.05, 0, 18, 90000000, 35, 140000, 230000, 3, "granos, minerales y carga a granel"),
        _transporte("Buque Ro-Ro", "maritimo", "buque_ro_ro", "no_perecedera", False, "combustoleo", 0.065, 0, 18, 45000000, 40, 120000, 210000, 4, "vehículos y maquinaria rodante"),
        _transporte("Buque tanque", "maritimo", "buque_tanque", "no_perecedera", False, "combustoleo", 0.045, 0, 18, 100000000, 32, 170000, 300000, 3, "líquidos, combustibles y químicos"),
    ]
)


def upsert_seed() -> None:
    db = SessionLocal()
    try:
        puntos = {}
        for data in PUNTOS_LOGISTICOS:
            data = _punto_con_coordenadas(data)
            punto = db.query(PuntoLogistico).filter(PuntoLogistico.nombre == data["nombre"]).first()
            if not punto:
                punto = PuntoLogistico(**data)
                db.add(punto)
                db.flush()
            else:
                for campo, valor in data.items():
                    setattr(punto, campo, valor)
                punto.activo = True
            puntos[punto.nombre] = punto

        for data in RUTAS_LEGADO:
            _upsert_ruta(db, data)

        for (
            origen_nombre,
            destino_nombre,
            distancia_km,
            casetas,
            trafico,
            riesgo,
            estado_carretera,
            inseguridad,
        ) in RUTAS_LOGISTICAS:
            origen = puntos[origen_nombre]
            destino = puntos[destino_nombre]
            data = {
                "nombre": f"{origen.nombre} - {destino.nombre}",
                "origen": origen.nombre,
                "destino": destino.nombre,
                "origen_id": origen.id,
                "destino_id": destino.id,
                "distancia_km": distancia_km,
                "casetas": casetas,
                "trafico": trafico,
                "riesgo": riesgo,
                "estado_carretera": estado_carretera,
                "inseguridad": inseguridad,
                "activa": True,
            }
            _upsert_ruta(db, data)

        _generar_rutas_automaticas(db)

        for data in TRANSPORTES:
            transporte = db.query(Transporte).filter(Transporte.nombre == data["nombre"]).first()
            if not transporte:
                db.add(Transporte(**data))
            else:
                for campo, valor in data.items():
                    setattr(transporte, campo, valor)
                transporte.activo = True

        db.commit()
        print("Datos de prueba cargados correctamente.")
    finally:
        db.close()


def _upsert_ruta(db, data: dict) -> None:
    ruta = db.query(Ruta).filter(Ruta.nombre == data["nombre"]).first()
    if not ruta:
        db.add(Ruta(**data))
        return

    for campo, valor in data.items():
        setattr(ruta, campo, valor)


def _punto_con_coordenadas(data: dict) -> dict:
    punto = data.copy()
    coordenadas = COORDENADAS_PUNTOS.get(punto["nombre"])
    if coordenadas:
        punto["latitud"], punto["longitud"] = coordenadas
    return punto


def _generar_rutas_automaticas(db) -> None:
    puntos_activos = (
        db.query(PuntoLogistico)
        .filter(PuntoLogistico.activo.is_(True))
        .order_by(PuntoLogistico.id.asc())
        .all()
    )

    for origen, destino in combinations(puntos_activos, 2):
        ruta_existente = _buscar_ruta_entre_puntos(db, origen, destino)
        if ruta_existente:
            _actualizar_ruta_existente_si_falta_caseta(
                ruta_existente,
                origen,
                destino,
            )
            continue

        distancia_km = _distancia_simulada(origen, destino)
        data = {
            "nombre": f"Ruta simulada {origen.nombre} - {destino.nombre}",
            "origen": origen.nombre,
            "destino": destino.nombre,
            "origen_id": origen.id,
            "destino_id": destino.id,
            "distancia_km": distancia_km,
            "casetas": _casetas_base(distancia_km),
            "trafico": 4 if distancia_km < 80 else 3,
            "riesgo": 2 if distancia_km < 300 else 3,
            "estado_carretera": 2 if distancia_km <= 500 else 3,
            "inseguridad": 2 if distancia_km < 200 else 3,
            "activa": True,
        }
        db.add(Ruta(**data))


def _buscar_ruta_entre_puntos(db, origen: PuntoLogistico, destino: PuntoLogistico):
    return (
        db.query(Ruta)
        .filter(
            (
                (Ruta.origen_id == origen.id)
                & (Ruta.destino_id == destino.id)
            )
            | (
                (Ruta.origen_id == destino.id)
                & (Ruta.destino_id == origen.id)
            )
            | (
                (Ruta.origen == origen.nombre)
                & (Ruta.destino == destino.nombre)
            )
            | (
                (Ruta.origen == destino.nombre)
                & (Ruta.destino == origen.nombre)
            )
        )
        .first()
    )


def _actualizar_ruta_existente_si_falta_caseta(
    ruta: Ruta,
    origen: PuntoLogistico,
    destino: PuntoLogistico,
) -> None:
    if ruta.origen == destino.nombre and ruta.destino == origen.nombre:
        punto_origen = destino
        punto_destino = origen
    else:
        punto_origen = origen
        punto_destino = destino

    if ruta.origen_id is None:
        ruta.origen_id = punto_origen.id
    if ruta.destino_id is None:
        ruta.destino_id = punto_destino.id

    if not ruta.distancia_km or ruta.distancia_km < 5:
        ruta.distancia_km = _distancia_simulada(punto_origen, punto_destino)

    if ruta.casetas is None or ruta.casetas <= 0:
        ruta.casetas = _casetas_base(ruta.distancia_km)

    ruta.activa = True


def _distancia_simulada(origen: PuntoLogistico, destino: PuntoLogistico) -> float:
    if _tiene_coordenadas(origen) and _tiene_coordenadas(destino):
        return round(max(_haversine_km(origen, destino) * 1.25, 5), 1)

    distancia_base = 70 if origen.estado == destino.estado else 320
    if origen.tipo != destino.tipo:
        distancia_base += 45
    return float(distancia_base)


def _haversine_km(origen: PuntoLogistico, destino: PuntoLogistico) -> float:
    latitud_origen = radians(origen.latitud)
    latitud_destino = radians(destino.latitud)
    delta_latitud = latitud_destino - latitud_origen
    delta_longitud = radians(destino.longitud - origen.longitud)
    factor = (
        sin(delta_latitud / 2) ** 2
        + cos(latitud_origen) * cos(latitud_destino) * sin(delta_longitud / 2) ** 2
    )
    return 6371 * 2 * asin(sqrt(factor))


def _tiene_coordenadas(punto: PuntoLogistico) -> bool:
    return punto.latitud is not None and punto.longitud is not None


def _casetas_base(distancia_km: float) -> float:
    return calcular_casetas_base_academicas(distancia_km)


if __name__ == "__main__":
    upsert_seed()
