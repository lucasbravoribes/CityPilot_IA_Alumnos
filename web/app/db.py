"""Acceso a PostgreSQL. Conexión mínima dada; funciones de negocio pendientes."""
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL", "")
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None


def ping_db():
    if engine is None:
        raise RuntimeError("Falta DATABASE_URL")
    with engine.connect() as conn:
        return conn.execute(text("SELECT 1")).scalar_one()


def guardar_solicitud(registro: dict) -> int:
    """TODO(ALUMNADO): INSERT parametrizado; devolver id de solicitud.

    La tabla existente es `solicitudes`. `registro` debe incluir: ciudad,
    pais, tipo_turismo, duracion_horas, preferencias, latitud, longitud,
    meteorologia, lugares, prompt_usado, itinerario, estado, duracion_ms,
    error_resumido, modo_demo y modo_modelo. Los diccionarios/listas van
    a columnas JSONB: podéis usar json.dumps(...) y CAST(:dato AS jsonb)
    o declarar el tipo JSONB en el parámetro enlazado.

    Pistas: with engine.begin() as conn; text(...); RETURNING id.
    Nunca concatenar strings de entrada dentro del SQL.
    """
    raise NotImplementedError("Implementa INSERT en PostgreSQL")


def obtener_estadisticas() -> dict:
    """TODO(ALUMNADO): total, agrupación por ciudad/tipo y nº errores."""
    raise NotImplementedError("Implementa SELECTs de analítica")


def obtener_ultimas_solicitudes(limite: int = 8) -> list[dict]:
    """TODO(ALUMNADO): últimas solicitudes sin mostrar claves ni secretos."""
    raise NotImplementedError("Implementa SELECT con ORDER BY fecha DESC LIMIT")
