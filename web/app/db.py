"""Acceso a PostgreSQL. Conexión mínima dada; funciones de negocio pendientes."""
import os
import json
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL", "")
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None


def ping_db():
    if engine is None:
        raise RuntimeError("Falta DATABASE_URL")
    with engine.connect() as conn:
        return conn.execute(text("SELECT 1")).scalar_one()


def _parametros_insert(registro: dict) -> dict:
    """Prepara los valores del INSERT a partir del diccionario del orquestador."""
    return {
        "ciudad": registro["ciudad"],
        "pais": registro.get("pais"),
        "tipo_turismo": registro["tipo_turismo"],
        "duracion_horas": registro["duracion_horas"],
        "preferencias": registro.get("preferencias") or "",
        "latitud": registro.get("latitud"),
        "longitud": registro.get("longitud"),
        "meteorologia": json.dumps(registro.get("meteorologia") or {}, ensure_ascii=False),
        "lugares": json.dumps(registro.get("lugares") or [], ensure_ascii=False),
        "prompt_usado": registro.get("prompt_usado"),
        "itinerario": registro.get("itinerario"),
        "estado": registro.get("estado", "ok"),
        "duracion_ms": registro.get("duracion_ms"),
        "error_resumido": registro.get("error_resumido"),
        "modo_demo": bool(registro.get("modo_demo", False)),
        "modo_modelo": registro.get("modo_modelo"),
    }


def guardar_solicitud(registro: dict) -> int:
    """Inserta una solicitud en `solicitudes` y devuelve su id."""
    if engine is None:
        raise RuntimeError("Falta DATABASE_URL")
    sql = text("""
        INSERT INTO solicitudes (
            ciudad, pais, tipo_turismo, duracion_horas, preferencias,
            latitud, longitud, meteorologia, lugares, prompt_usado,
            itinerario, estado, duracion_ms, error_resumido,
            modo_demo, modo_modelo
        ) VALUES (
            :ciudad, :pais, :tipo_turismo, :duracion_horas, :preferencias,
            :latitud, :longitud, CAST(:meteorologia AS jsonb), CAST(:lugares AS jsonb),
            :prompt_usado, :itinerario, :estado, :duracion_ms, :error_resumido,
            :modo_demo, :modo_modelo
        )
        RETURNING id
    """)
    with engine.begin() as conn:
        return conn.execute(sql, _parametros_insert(registro)).scalar_one()


def obtener_estadisticas() -> dict:
    """Métricas para el panel y para GET /api/estadisticas (todo desde PostgreSQL).

    Convenio con el orquestador: estado 'ok' = éxito, 'error' = fallo.
    """
    if engine is None:
        raise RuntimeError("Falta DATABASE_URL")
    with engine.connect() as conn:
        resumen = conn.execute(text("""
            SELECT COUNT(*)                                   AS total,
                   COUNT(DISTINCT ciudad)                     AS ciudades_distintas,
                   COUNT(*) FILTER (WHERE estado = 'error')   AS errores
            FROM solicitudes
        """)).mappings().one()
        por_ciudad = conn.execute(text("""
            SELECT ciudad, COUNT(*) AS total
            FROM solicitudes
            GROUP BY ciudad
            ORDER BY total DESC, ciudad
            LIMIT 5
        """)).mappings().all()
        por_tipo = conn.execute(text("""
            SELECT tipo_turismo, COUNT(*) AS total
            FROM solicitudes
            GROUP BY tipo_turismo
            ORDER BY total DESC, tipo_turismo
        """)).mappings().all()
    return {
        "total": resumen["total"],
        "ciudades_distintas": resumen["ciudades_distintas"],
        "errores": resumen["errores"],
        "por_ciudad": [dict(f) for f in por_ciudad],
        "por_tipo": [dict(f) for f in por_tipo],
    }


def obtener_ultimas_solicitudes(limite: int = 8) -> list[dict]:
    """Últimas solicitudes, más recientes primero (solo columnas seguras para mostrar)."""
    if engine is None:
        raise RuntimeError("Falta DATABASE_URL")
    limite = max(1, min(int(limite), 50))
    with engine.connect() as conn:
        filas = conn.execute(text("""
            SELECT id, fecha, ciudad, tipo_turismo, duracion_horas,
                   estado, modo_demo, modo_modelo, duracion_ms
            FROM solicitudes
            ORDER BY fecha DESC, id DESC
            LIMIT :limite
        """), {"limite": limite}).mappings().all()
    return [dict(f) for f in filas]



