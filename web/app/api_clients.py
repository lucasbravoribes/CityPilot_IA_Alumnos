"""Clientes HTTP de datos públicos: Open-Meteo y OpenStreetMap/Overpass.

Las funciones exponen contratos pequeños y normalizados para que el resto
 de la aplicación no dependa del JSON específico de cada proveedor.
"""
import json
import math
import os
from pathlib import Path

import requests

GEO_URL = os.getenv("OPEN_METEO_GEO_URL", "https://geocoding-api.open-meteo.com/v1/search")
METEO_URL = os.getenv("OPEN_METEO_WEATHER_URL", "https://api.open-meteo.com/v1/forecast")
OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")

HTTP_TIMEOUT = 8
OVERPASS_TIMEOUT = 25
RADIO_METROS = 2500
MAX_LUGARES = 12


class SinResultadosError(LookupError):
    """El proveedor respondió correctamente, pero no encontró coincidencias."""


# Etiquetas controladas por la aplicación. Nunca se interpolan valores del usuario.
ETIQUETAS_POR_TIPO = {
    "cultural": {
        "tourism": ("museum", "attraction", "gallery"),
        "historic": ("monument", "castle", "memorial"),
    },
    "gastronomica": {
        "amenity": ("restaurant", "cafe", "food_court"),
    },
    "naturaleza": {
        "leisure": ("park", "garden"),
    },
    "familiar": {
        "tourism": ("attraction", "zoo"),
        "leisure": ("park", "playground"),
    },
}


def _validar_coordenadas(lat: float, lon: float) -> tuple[float, float]:
    """Comprueba y convierte coordenadas antes de construir peticiones."""
    try:
        latitud, longitud = float(lat), float(lon)
    except (TypeError, ValueError) as exc:
        raise ValueError("La latitud y longitud deben ser números.") from exc

    if not (math.isfinite(latitud) and math.isfinite(longitud)):
        raise ValueError("Las coordenadas deben ser valores finitos.")
    if not -90 <= latitud <= 90 or not -180 <= longitud <= 180:
        raise ValueError("Las coordenadas están fuera de rango.")
    return latitud, longitud


def geocodificar(ciudad: str) -> dict:
    """Busca una ciudad en España y devuelve ciudad, país y coordenadas.

    Lanza SinResultadosError si la respuesta HTTP es correcta pero no contiene
    coincidencias. Los errores HTTP y de conexión de requests se propagan.
    """
    if not isinstance(ciudad, str) or not ciudad.strip():
        raise ValueError("Debes indicar una ciudad.")

    respuesta = requests.get(
        GEO_URL,
        params={
            "name": ciudad.strip(),
            "count": 1,
            "language": "es",
            "countryCode": "ES",
        },
        timeout=HTTP_TIMEOUT,
    )
    respuesta.raise_for_status()
    contenido = respuesta.json()
    resultados = contenido.get("results") or []

    if not resultados:
        raise SinResultadosError(f"No se encontraron resultados para '{ciudad.strip()}'.")

    resultado = resultados[0]
    try:
        nombre = str(resultado["name"]).strip()
        pais = str(resultado["country"]).strip()
        latitud, longitud = _validar_coordenadas(
            resultado["latitude"], resultado["longitude"]
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Open-Meteo devolvió datos de geocodificación incompletos.") from exc

    if not nombre or not pais:
        raise ValueError("Open-Meteo devolvió una ciudad o país vacío.")

    return {"ciudad": nombre, "pais": pais, "lat": latitud, "lon": longitud}


def obtener_meteorologia(lat: float, lon: float) -> dict:
    """Obtiene las condiciones meteorológicas actuales para unas coordenadas."""
    latitud, longitud = _validar_coordenadas(lat, lon)
    respuesta = requests.get(
        METEO_URL,
        params={
            "latitude": latitud,
            "longitude": longitud,
            "current": "temperature_2m,precipitation,weather_code",
            "timezone": "auto",
        },
        timeout=HTTP_TIMEOUT,
    )
    respuesta.raise_for_status()
    contenido = respuesta.json()
    actual = contenido.get("current") or {}

    try:
        temperatura = float(actual["temperature_2m"])
        precipitacion = float(actual["precipitation"])
        codigo = int(actual["weather_code"])
        instante = str(actual["time"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Open-Meteo no devolvió todos los datos meteorológicos actuales.") from exc

    if not all(math.isfinite(valor) for valor in (temperatura, precipitacion)) or not instante:
        raise ValueError("Open-Meteo devolvió datos meteorológicos no válidos.")

    return {
        "temperatura_c": temperatura,
        "precipitacion_mm": precipitacion,
        "codigo_tiempo": codigo,
        "instante": instante,
    }


def _construir_consulta_overpass(lat: float, lon: float, tipo: str) -> str:
    """Construye QL únicamente con etiquetas incluidas en la lista permitida."""
    if tipo not in ETIQUETAS_POR_TIPO:
        raise ValueError(
            "Tipo de turismo no válido. Usa: cultural, gastronomica, naturaleza o familiar."
        )

    consultas = []
    for clave, valores in ETIQUETAS_POR_TIPO[tipo].items():
        expresion = "|".join(valores)
        consultas.append(
            f'nwr["{clave}"~"^({expresion})$"](around:{RADIO_METROS},{lat},{lon});'
        )

    return (
        "[out:json][timeout:20];\n("
        + "\n".join(consultas)
        + f"\n);\nout center tags {MAX_LUGARES};"
    )


def obtener_lugares(lat: float, lon: float, tipo: str) -> list[dict]:
    """Recupera hasta 12 lugares OSM próximos y devuelve una lista normalizada.

    Los nodos usan lat/lon; ways y relations usan center.lat/center.lon.
    Una respuesta sin elementos se representa como [] (no como error HTTP).
    """
    latitud, longitud = _validar_coordenadas(lat, lon)
    consulta = _construir_consulta_overpass(latitud, longitud, tipo)

    respuesta = requests.post(
        OVERPASS_URL,
        data={"data": consulta},
        timeout=OVERPASS_TIMEOUT,
    )
    respuesta.raise_for_status()
    contenido = respuesta.json()
    elementos = contenido.get("elements") or []

    lugares = []
    nombres_vistos = set()
    for elemento in elementos:
        etiquetas = elemento.get("tags") or {}
        nombre = etiquetas.get("name")
        if not isinstance(nombre, str) or not nombre.strip():
            continue

        if elemento.get("type") == "node":
            coordenadas = elemento
        else:
            coordenadas = elemento.get("center") or {}

        try:
            lugar_lat, lugar_lon = _validar_coordenadas(
                coordenadas["lat"], coordenadas["lon"]
            )
        except (KeyError, TypeError, ValueError):
            continue

        nombre = nombre.strip()
        clave_nombre = nombre.casefold()
        if clave_nombre in nombres_vistos:
            continue
        nombres_vistos.add(clave_nombre)

        categoria = next(
            (
                str(etiquetas[clave])
                for clave in ETIQUETAS_POR_TIPO[tipo]
                if clave in etiquetas
            ),
            tipo,
        )
        lugares.append(
            {
                "nombre": nombre,
                "categoria": categoria,
                "lat": lugar_lat,
                "lon": lugar_lon,
                "fuente": "OpenStreetMap",
                "demo": False,
            }
        )
        if len(lugares) >= MAX_LUGARES:
            break

    return lugares


def cargar_fixture_lugares() -> list[dict]:
    """Utilidad entregada para simular Overpass durante pruebas sin Internet.

    Los lugares son FICTICIOS y deben identificarse como DEMO en la UI.
    """
    file_path = Path("/fixtures/puntos_demo.json")
    if not file_path.exists():
        file_path = Path(__file__).resolve().parents[2] / "fixtures/puntos_demo.json"
    return json.loads(file_path.read_text(encoding="utf-8"))["lugares"]
