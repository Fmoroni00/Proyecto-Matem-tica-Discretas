from math import radians, sin, cos, sqrt, atan2

from estructuras.grafo import Grafo

NODOS_COORDS = {
    "Cercado de Lima": {"lat": -12.0464, "lng": -77.0428},
    "Jesús María": {"lat": -12.0719, "lng": -77.0431},
    "Lince": {"lat": -12.0876, "lng": -77.0364},
    "San Isidro": {"lat": -12.1040, "lng": -77.0348},
    "Miraflores": {"lat": -12.1203, "lng": -77.0282},
    "Barranco": {"lat": -12.1406, "lng": -77.0214},
    "Surquillo": {"lat": -12.1142, "lng": -77.0177},
    "San Borja": {"lat": -12.1086, "lng": -77.0023},
    "Surco": {"lat": -12.1339, "lng": -76.9931},
    "La Molina": {"lat": -12.0794, "lng": -76.9397},
    "Pueblo Libre": {"lat": -12.0740, "lng": -77.0615},
    "San Miguel": {"lat": -12.0773, "lng": -77.0907},
    "Callao": {"lat": -12.0566, "lng": -77.1181},
    "Los Olivos": {"lat": -11.9570, "lng": -77.0760},
    "San Martín de Porres": {"lat": -12.0000, "lng": -77.0700},
    "Comas": {"lat": -11.9440, "lng": -77.0620},
    "Independencia": {"lat": -11.9930, "lng": -77.0530},
    "Carabayllo": {"lat": -11.9050, "lng": -77.0310},
}

FACTOR_CORRECCION_CARRETERA = 1.4


def _distancia_haversine(lat1, lng1, lat2, lng2):
    """Calcula la distancia en km entre dos puntos usando Haversine y un factor de corrección."""
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lng2 - lng1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distancia_aerea = R * c
    return round(distancia_aerea * FACTOR_CORRECCION_CARRETERA, 2)


def estimar_tiempo_viaje(distancia_km: float) -> int:
    """Estima un tiempo de viaje razonable para Lima."""
    if distancia_km <= 0:
        return 0

    velocidad_promedio_kmh = 24
    tiempo_min = (distancia_km / velocidad_promedio_kmh) * 60
    return max(8, int(round(tiempo_min)))


def crear_grafo_lima() -> Grafo:
    g = Grafo()
    edges = [
        ("Cercado de Lima", "Jesús María", 3),
        ("Cercado de Lima", "Lince", 4),
        ("Lince", "San Isidro", 2),
        ("San Isidro", "Miraflores", 3),
        ("Miraflores", "Barranco", 3),
        ("Miraflores", "Surquillo", 2),
        ("Surquillo", "San Borja", 3),
        ("San Borja", "Surco", 4),
        ("Surco", "La Molina", 6),
        ("Cercado de Lima", "Pueblo Libre", 4),
        ("Pueblo Libre", "San Miguel", 3),
        ("San Miguel", "Callao", 7),
        ("Jesús María", "Lince", 2),
        ("San Isidro", "San Borja", 4),
        ("Los Olivos", "San Martín de Porres", 3),
        ("San Martín de Porres", "Independencia", 3),
        ("San Martín de Porres", "Comas", 4),
        ("Comas", "Carabayllo", 5),
        ("Independencia", "Jesús María", 6),
        ("San Martín de Porres", "Cercado de Lima", 7),
    ]

    for u, v, w in edges:
        g.agregar_arista(u, v, w, bidireccional=True)
    return g


GRAFO = crear_grafo_lima()


def calcular_mejor_ruta(origen: str, destino: str):
    """Devuelve la ruta más corta con una distancia realista basada en coordenadas."""
    distancia_total, path = GRAFO.dijkstra(origen, destino)

    if not path or distancia_total == float("inf"):
        return float("inf"), []

    if len(path) >= 2:
        distancia_real = 0.0
        for nodo_origen, nodo_destino in zip(path, path[1:]):
            coords_origen = NODOS_COORDS.get(nodo_origen)
            coords_destino = NODOS_COORDS.get(nodo_destino)
            if coords_origen and coords_destino:
                distancia_real += _distancia_haversine(
                    coords_origen["lat"], coords_origen["lng"],
                    coords_destino["lat"], coords_destino["lng"],
                )

        if distancia_real > 0:
            return round(distancia_real, 2), path

    return round(distancia_total, 2), path
