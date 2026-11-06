import time
import os
from app.api_clients import geocodificar, obtener_meteorologia, obtener_lugares
from app.llm import generar_itinerario
from app.db import guardar_solicitud

def procesar_solicitud(datos: dict):
    """
    Orquesta el flujo completo de CityPilot IA:
    1. Valida los datos de entrada de forma estricta.
    2. Realiza llamadas reales a servicios externos (Geocodificación, Clima, Lugares).
    3. Consulta al LLM (Cohere o mock según configuración) para generar el itinerario.
    4. Guarda la solicitud y el resultado en PostgreSQL.
    5. Devuelve el contrato de respuesta estructurado o gestiona errores específicos.
    """
    inicio = time.time()
    
    # --- 1. VALIDACIÓN ESTRICTA DE ENTRADA ---
    if not isinstance(datos, dict):
        raise ValueError("Formato de datos no válido. Se esperaba un diccionario JSON.")
    
    ciudad = datos.get("ciudad")
    tipo = datos.get("tipo")
    duracion = datos.get("duracion")
    preferencias = datos.get("preferencias", "")

    if not ciudad or not isinstance(ciudad, str) or not ciudad.strip():
        raise ValueError("El campo 'ciudad' es obligatorio y debe ser un texto válido.")
    
    tipos_validos = ["cultural", "gastronomico", "naturaleza", "familiar"]
    if not tipo or tipo not in tipos_validos:
        raise ValueError(f"El campo 'tipo' es obligatorio y debe ser uno de los siguientes: {', '.join(tipos_validos)}.")

    try:
        duracion_int = int(duracion)
        if duracion_int not in [2, 4, 6]:
            raise ValueError("La 'duracion' debe ser exactamente 2, 4 o 6 horas.")
    except (TypeError, ValueError):
        raise ValueError("El campo 'duracion' debe ser un número entero válido (2, 4 o 6).")

    try:
        # --- 2. LLAMADAS REALES A APIS EXTERNAS (Proveedor) ---
        try:
            coordenadas = geocodificar(ciudad.strip())
        except Exception as e:
            raise RuntimeError(f"Error en el servicio de geocodificación para la ciudad '{ciudad}': {str(e)}")

        try:
            clima = obtener_meteorologia(coordenadas)
        except Exception as e:
            raise RuntimeError(f"Error al obtener la meteorología del proveedor externo: {str(e)}")

        try:
            lugares = obtener_lugares(coordenadas, tipo, duracion_int)
        except Exception as e:
            raise RuntimeError(f"Error al consultar los lugares de interés (Overpass): {str(e)}")

        # --- 3. GENERACIÓN CON LLM (Cohere / Mock) ---
        try:
            prompt_respuesta = generar_itinerario(
                ciudad=ciudad,
                tipo=tipo,
                duracion=duracion_int,
                clima=clima,
                lugares=lugares,
                preferencias=preferencias
            )
        except Exception as e:
            raise RuntimeError(f"Error al generar el itinerario con el modelo de lenguaje: {str(e)}")

        # --- 4. CONSTRUCCIÓN DEL CONTRATO DE RESPUESTA ---
        duracion_peticion = round(time.time() - inicio, 2)
        
        # Extraer texto y modo del modelo de forma robusta
        if isinstance(prompt_respuesta, dict):
            texto_itinerario = prompt_respuesta.get("texto", str(prompt_respuesta))
            modo_modelo = prompt_respuesta.get("modo", os.getenv("LLM_MODE", "unknown"))
        else:
            texto_itinerario = str(prompt_respuesta)
            modo_modelo = os.getenv("LLM_MODE", "unknown")

        resultado = {
            "ciudad": ciudad.strip().capitalize(),
            "tipo": tipo,
            "duracion": duracion_int,
            "preferencias": preferencias,
            "clima": clima,
            "lugares": lugares,
            "itinerario": texto_itinerario,
            "modo_modelo": modo_modelo,
            "simulado": True if modo_modelo == "mock" else False,
            "tiempo_ejecucion": duracion_peticion
        }

        # --- 5. PERSISTENCIA EN POSTGRESQL ---
        try:
            guardar_solicitud(datos, resultado)
        except Exception as e:
            # La base de datos registra el fallo pero no bloquea la entrega si los datos son correctos
            print(f"[Advertencia] No se pudo persistir la solicitud en PostgreSQL: {str(e)}")

        return resultado, None

    except ValueError as ve:
        # Errores de validación de cliente (400)
        return None, f"Error de validación: {str(ve)}"
    except RuntimeError as re:
        # Errores de proveedores externos / infraestructura (502/503)
        return None, f"Error de proveedor externo: {str(re)}"
    except Exception as e:
        # Error interno general no contemplado (500)
        return None, f"Error interno inesperado en el orquestador: {str(e)}"