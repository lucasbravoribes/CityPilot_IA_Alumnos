# Guía técnica de trabajo: QUÉ debe hacer cada pieza, sin soluciones

> **Este documento NO es código que haya que copiar.** Describe entradas, salidas, casos de error y criterios de prueba. Debéis decidir y escribir las instrucciones Python, las consultas SQL, el HTML y los prompts. Empezad con una versión sencilla que funcione y ampliad después. El profesor puede explicar conceptos, pero no programará las funciones por vosotros.

## Módulo 1 — `web/app/api_clients.py`: datos públicos

### `geocodificar(ciudad)`
- **Recibe** texto introducido por el usuario (ej. `Valencia`), previamente validado.
- **Tiene que hacer** una consulta HTTP a Open-Meteo Geocoding; comprobar el código HTTP; interpretar el JSON; elegir una coincidencia razonable y extraer cuatro campos normalizados: `ciudad`, `pais`, `lat`, `lon`.
- **No debe** utilizar coordenadas escritas a mano para fingir una respuesta ni devolver un JSON bruto enorme.
- **Comprobación**: una ciudad válida da latitud/longitud numéricas; una búsqueda inexistente no provoca `IndexError` ni muestra un traceback al usuario.

### `obtener_meteorologia(lat,lon)`
- **Recibe** las coordenadas del paso anterior.
- **Tiene que hacer** una consulta a Open-Meteo Forecast (apartado `current`) y devolver `temperatura_c`, `precipitacion_mm`, `codigo_tiempo` e `instante`.
- **No debe** tratar un campo ausente como si fuera un 0 real; tampoco inventar previsiones futuras.
- **Comprobación**: comparar el JSON original de la API con los cuatro campos devueltos por vuestra función; simular un error HTTP.

### `obtener_lugares(lat,lon,tipo)`
- **Recibe** coordenadas y uno de cuatro tipos válidos (`cultural`, `gastronomica`, `naturaleza`, `familiar`).
- **Tiene que hacer** construir la consulta Overpass correspondiente al tipo, recuperar lugares cercanos, seleccionar solo lugares con nombre y normalizar una lista de diccionarios con `nombre`, `categoria`, `lat`, `lon`, `fuente`, `demo`.
- **No debe** incluir etiquetas no autorizadas introducidas por el usuario en una consulta QL ni inventar sitios. Si recibe geometrías no puntuales, buscar dónde se hallan las coordenadas del centro.
- **Comprobación**: mostrar una muestra de 3 lugares, detectar coordenadas que faltan y razonar qué haríais si Overpass devuelve una lista vacía o responde 504.

## Módulo 2 — `web/app/llm.py`: prompt y conexión al modelo

### `generar_itinerario(contexto)`
- **Recibe** ciudad, duración, preferencias, tipo, meteorología y lista de lugares obtenidos en el módulo 1.
- **Tenéis que diseñar vuestro propio prompt**. Debe permitir al modelo saber qué rol tiene, qué información se considera verificable, qué debe producir y qué restricciones no puede incumplir.
- **Salida esperada:** texto legible con una ruta de unas 3-5 paradas escogidas **solo** de la lista recibida; una justificación relacionada con el clima; una consideración de duración y preferencias; y una nota explícita cuando no existan sitios suficientes o haya datos de demostración.
- **Preguntas que debéis resolver con un experimento:** ¿el modelo cita algún lugar que no está en la lista? ¿cambia la propuesta si el clima es lluvioso? ¿respeta 2 horas frente a 6? ¿explica datos insuficientes en lugar de completar con su imaginación?
- **Entrega de evidencia:** versión inicial del prompt (o enlace seguro), resultado obtenido, fallo/limitación y modificación que decidisteis realizar. El texto de los prompts **no se facilita**. Tampoco se facilita la implementación de la llamada HTTP a Cohere.

## Módulo 3 — `web/app/orchestrator.py`: unir todo

### `procesar_solicitud(ciudad,tipo_turismo,duracion_horas,preferencias)`
- **Tiene que hacer** validar entradas → pedir geocodificación → obtener clima → recuperar puntos → preparar contexto → solicitar itinerario → guardar resultado → devolver un diccionario con información para HTML y JSON.
- **Decisiones de diseño**: dónde capturar excepciones, cómo distinguir errores propios (entrada incorrecta) de errores del proveedor, cómo medir la duración, qué almacenar si algo falla.
- **Comprobación**: una petición válida desde web y la misma petición desde API obtienen una estructura equivalente y utilizan la misma función. Una petición inválida no consume servicios externos.

## Módulo 4 — `web/app/main.py` y `templates/`: interfaces

- **Formulario `index.html`:** ciudad como texto; tipo mediante lista de cuatro opciones; duración mediante lista 2/4/6; preferencias opcionales; botón. Usad nombres de campos que coincidan con el contrato. No se entrega ningún `<form>` completo.
- **`POST /planificar`:** leer formulario, llamar al orquestador y pasar su salida a `resultado.html`.
- **`POST /api/planificar`:** leer un JSON con los mismos campos, llamar al mismo orquestador y responder JSON. Los errores de validación deben ser 400 y los fallos de proveedores no deben esconderse en un 200.
- **`resultado.html`:** clima, nombres de lugares, itinerario y señal visible si los datos o el modelo son simulados. Si faltan datos reales, decirlo.
- **`GET /analitica`:** pedir las estadísticas de PostgreSQL y mostrarlas (no utilizar datos escritos a mano).
- **`/analitica/grafico.png`:** construir una gráfica con datos agrupados consultados en Postgres; entregar PNG generada en memoria.
- **Comprobación**: cambio de ciudad/tipo cambia la consulta y el contenido; nueva petición produce una fila adicional y el dashboard lo refleja.

## Módulo 5 — `web/app/db.py`: persistir y analizar

### `guardar_solicitud(registro)`
- **Recibe** los datos de usuario, metadatos, contexto y resultado del flujo.
- **Tiene que hacer** inserción parametrizada en `solicitudes` y devolver el identificador creado. Guardar diccionarios/listas en columnas JSONB sin convertirlos a texto visible en el dashboard.
- **Comprobación**: ejecutar una consulta SELECT y confirmar que aparecen el prompt, los lugares y el resultado correctos; nunca credenciales.

### `obtener_estadisticas()` y `obtener_ultimas_solicitudes(limite)`
- **Tienen que hacer** contar solicitudes, agrupar por ciudad y tipo, calcular errores, recuperar últimas 8 con orden por fecha.
- **Comprobación**: solicitar varias ciudades y confirmar que los números cambian al refrescar el panel.

## Módulo 6 — Jupyter + pruebas

En `notebooks/01_validacion.ipynb` completar y ejecutar las celdas pendientes: dos APIs Open-Meteo encadenadas; `POST /api/planificar`; consulta a Postgres; entrada inválida con respuesta 400. **No basta con el código: dejad salidas visibles.** En `web/tests/` redactad dos pruebas automatizadas propias distintas de los tests base. Si usáis IA para diseñar casos, explicad qué aportó y qué comprobasteis manualmente.

## ¿Cuándo está realmente terminado?

Otro compañero puede clonar el repositorio, crear su `.env`, arrancar Compose y demostrar un ciclo completo sin modificar datos a mano. Debe poder observar el resultado, la fila SQL y el dashboard; comprobar errores controlados; revisar los PR y consultar la memoria de IA de cada miembro. La trazabilidad y la comprensión son tan importantes como que aparezca una página bonita.
