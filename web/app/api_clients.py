"""Clientes HTTP de datos públicos. Se entregan los contratos, NO la solución."""
import json
import os
from pathlib import Path
import requests

GEO_URL = os.getenv("OPEN_METEO_GEO_URL", "https://geocoding-api.open-meteo.com/v1/search")
METEO_URL = os.getenv("OPEN_METEO_WEATHER_URL", "https://api.open-meteo.com/v1/forecast")
OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")


def geocodificar(ciudad: str) -> dict:
    """TODO(ALUMNADO).

    Entrada: 'Valencia'. Salida normalizada: {'ciudad': 'Valencia',
    'pais': 'España', 'lat': 39.47, 'lon': -0.38} (números ilustrativos).
    Usar Open-Meteo Geocoding y controlar búsqueda sin resultados.
    Restricción: peticiones con timeout, filtrando countryCode='ES' si se
    decide limitar a España.
    """
    raise NotImplementedError("Implementa búsqueda de coordenadas")


def obtener_meteorologia(lat: float, lon: float) -> dict:
    """TODO(ALUMNADO).

    Devolver, como mínimo: temperatura_c, precipitacion_mm,
    codigo_tiempo, instante. Seleccionar current=temperature_2m,
    precipitation,weather_code e incluir timezone=auto.
    """
    raise NotImplementedError("Implementa consulta meteorológica")


def obtener_lugares(lat: float, lon: float, tipo: str) -> list[dict]:
    """TODO(ALUMNADO).

    Consultar un radio urbano acotado de Overpass/OSM (2-3 km).
    Filtrar según tipo: cultural, gastronomica, naturaleza, familiar.
    Normalizar a [{nombre, categoria, lat, lon, fuente, ...}], máximo
    8-12 lugares. Gestionar nodos (lat/lon) y ways/relations (center).
    Nunca introducir valores libres del usuario en una consulta QL.
    """
    raise NotImplementedError("Implementa consulta de puntos de interés")


def cargar_fixture_lugares() -> list[dict]:
    """Utilidad entregada para simular Overpass durante pruebas sin Internet.

    Los lugares son FICTICIOS y deben identificarse como DEMO en la UI.
    """
    file_path = Path("/fixtures/puntos_demo.json")
    if not file_path.exists():
        file_path = Path(__file__).resolve().parents[2] / "fixtures/puntos_demo.json"
    return json.loads(file_path.read_text(encoding="utf-8"))["lugares"]
