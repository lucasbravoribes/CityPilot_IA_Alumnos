"""Adaptador Cohere. El PROMPT lo redacta el alumnado."""
import os
import requests

LLM_MODE = os.getenv("LLM_MODE", "mock").lower()
COHERE_MODEL = os.getenv("COHERE_MODEL", "command-r7b-12-2024")


def generar_itinerario(contexto: dict) -> tuple[str, str]:
    """Devuelve (texto_itinerario, prompt_usado).

    `contexto` incluye: ciudad, tipo_turismo, duracion_horas,
    preferencias, meteorologia y lista de lugares REALES de la fuente.
    """
    if LLM_MODE == "mock":
        return _simulador(contexto), "[SIMULADOR: sin llamada a modelo]"

    if LLM_MODE != "cohere":
        raise ValueError("LLM_MODE debe ser 'mock' o 'cohere'")

    api_key = os.getenv("COHERE_API_KEY", "")
    if not api_key:
        raise RuntimeError("Falta COHERE_API_KEY (pedirla al docente)")

    # TODO(ALUMNADO): redactar VUESTRO PROPIO prompt en castellano.
    # Debe pedir 3-5 paradas del listado verificable, justificar cambios
    # por clima, respetar duración/preferencias, no inventar horarios ni
    # ubicaciones y declarar si no hay suficientes datos.
    # TODO(ALUMNADO): descubrir en la documentación Cohere Chat v2
    # cómo autenticar la petición, construir el JSON de entrada,
    # enviar un mensaje de usuario y extraer el texto devuelto.
    # Documentad un primer intento y al menos una mejora del prompt.
    # Comprobad errores 401/429, respuesta vacía y timeout.
    # No guardar nunca claves ni cabeceras privadas.
    raise NotImplementedError("Implementa llamada al modelo Cohere")


def _simulador(contexto: dict) -> str:
    """Salida no generativa para pruebas y para cuando no hay credenciales."""
    lugares = contexto.get("lugares") or []
    ciudad = contexto.get("ciudad", "la ciudad")
    tipo = contexto.get("tipo_turismo", "libre")
    nombres = [x.get("nombre", "Lugar sin nombre") for x in lugares[:4]]
    visitas = "\n".join(f"{i}. {nombre}" for i, nombre in enumerate(nombres, 1))
    if not visitas:
        visitas = "No hay lugares verificados disponibles."
    return f"[MODO SIMULACIÓN - NO ES IA]\nPlan {tipo} en {ciudad}:\n{visitas}"
