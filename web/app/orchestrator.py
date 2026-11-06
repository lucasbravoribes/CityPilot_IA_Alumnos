"""Punto ÚNICO de integración para web y API JSON. Pendiente del alumnado."""
from app import api_clients, db, llm

TIPOS_VALIDOS = {"cultural", "gastronomica", "naturaleza", "familiar"}
DURACIONES_VALIDAS = {2, 4, 6}


def procesar_solicitud(ciudad: str, tipo_turismo: str, duracion_horas: int, preferencias: str = "") -> dict:
    """TODO(ALUMNADO): implementar todo el recorrido.

    1) Validación (ciudad no vacía, tipo permitido, duración 2/4/6).
    2) Geocodificar la ciudad y consultar clima actual.
    3) Consultar lugares reales; si falla Overpass, utilizar fixture
       SOLAMENTE para demostrar flujo, marcando 'demo': True.
    4) Preparar el contexto y llamar a llm.generar_itinerario.
    5) Guardar entradas, respuestas, prompt, resultado, éxito/error,
       duración y el modo de datos en PostgreSQL.
    6) Devolver contrato consistente a ambas rutas Flask.

    Salida orientativa:
      {'ciudad': ..., 'tipo_turismo': ..., 'meteorologia': {...},
       'lugares': [...], 'itinerario': ..., 'modo_demo': False,
       'solicitud_id': 1}

    IMPORTANTE: ni el modelo ni los mocks son la fuente de lugares.
    Los datos de interés proceden de Overpass; el modelo los ORGANIZA.
    """
    raise NotImplementedError("Implementa el flujo de integración")
