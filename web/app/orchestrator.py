import time
# Importaciones preparadas para cuando tus compañeros hagan merge de sus ramas:
# from app.api_clients import geocodificar, obtener_meteorologia, obtener_lugares
# from app.llm import generar_itinerario
# from app.db import guardar_solicitud

def procesar_solicitud(datos: dict):
    inicio = time.time()
    
    # 1. Validación básica
    if not datos.get("ciudad") or not datos.get("tipo") or not datos.get("duracion"):
        return None, "Faltan campos obligatorios"

    try:
        # --- ZONA DE INTEGRACIÓN (Aquí llamaremos a las funciones de tus compañeros) ---
        # 2. Datos externos (Dev 1)
        # coordenadas = geocodificar(datos["ciudad"])
        # clima = obtener_meteorologia(coordenadas)
        # lugares = obtener_lugares(coordenadas, datos["tipo"])
        
        # MOCKS (Bórralos cuando Dev 1 termine)
        coordenadas = {"lat": 39.4697, "lon": -0.3773}
        clima = {"temperatura": 22, "condicion": "Soleado"}
        lugares = [
            {"nombre": "Plaza de Toros", "lat": 39.4666, "lon": -0.3774},
            {"nombre": "Ciudad de las Artes", "lat": 39.4534, "lon": -0.3470}
        ]

        # 3. LLM Cohere (Dev 2)
        # prompt_respuesta = generar_itinerario(datos, clima, lugares)
        
        # MOCK (Bórralo cuando Dev 2 termine)
        prompt_respuesta = {"texto": "Os sugiero empezar en la Plaza de Toros...", "modo": "mock"}

        # 4. Construir resultado final
        duracion_peticion = round(time.time() - inicio, 2)
        
        resultado = {
            "ciudad": datos["ciudad"],
            "clima": clima,
            "lugares": lugares,
            "itinerario": prompt_respuesta["texto"],
            "modo_modelo": prompt_respuesta["modo"],
            "simulado": True if prompt_respuesta["modo"] == "mock" else False,
            "tiempo_ejecucion": duracion_peticion
        }

        # 5. Persistencia (Dev 4)
        # guardar_solicitud(datos, resultado)

        return resultado, None

    except Exception as e:
        # En producción no mostraríamos el stack trace al usuario, solo un error genérico[cite: 6]
        return None, f"Error interno procesando la ruta: {str(e)}"