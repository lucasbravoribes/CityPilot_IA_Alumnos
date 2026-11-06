# Contratos y pistas de las APIs (sin funciones resueltas)

## A. Open-Meteo Geocoding · ciudad → coordenadas

- Documentación: https://open-meteo.com/en/docs/geocoding-api
- URL: `https://geocoding-api.open-meteo.com/v1/search`
- Método: `GET`.
- Parámetros recomendados: `name=Valencia`, `count=1`, `language=es`, `countryCode=ES`.
- Buscar la primera entrada de `results`; las claves interesantes son `name`, `country`, `latitude`, `longitude`. Si no existe `results`, no existe coincidencia.
- Contrato de salida de vuestra función: `{'ciudad': str, 'pais': str, 'lat': float, 'lon': float}`. No paséis todo el JSON bruto al resto de la aplicación.

Ejemplo mínimo de **patrón HTTP**, no solución completa:

```python
r = requests.get(url, params=parametros, timeout=8)
r.raise_for_status()
contenido = r.json()
# TODO: localizar, validar y transformar los campos útiles
```

## B. Open-Meteo Forecast · coordenadas → condiciones actuales

- Documentación: https://open-meteo.com/en/docs
- URL: `https://api.open-meteo.com/v1/forecast`
- Método: `GET`.
- Parámetros: `latitude`, `longitude`, `current=temperature_2m,precipitation,weather_code`, `timezone=auto`.
- Leer de `current` el tiempo de observación, temperatura en grados C, precipitación en mm y código meteorológico WMO (por ejemplo, código 0 suele representar cielo despejado; consultar tabla oficial).
- Contrato normalizado: `{'temperatura_c': float, 'precipitacion_mm': float, 'codigo_tiempo': int, 'instante': str}`.
- **Actual vs mañana:** la actividad es «hoy», por eso la versión obligatoria usa `current`. No inventéis la previsión hora por hora.

## C. OpenStreetMap / Overpass · coordenadas → lugares cercanos

- Wiki: https://wiki.openstreetmap.org/wiki/Overpass_API
- URL: `https://overpass-api.de/api/interpreter` (configurable mediante `.env`).
- Método: `POST`, con campo `data` que contiene texto Overpass QL. La API es pública y puede fallar por carga: `timeout` HTTP y **un intento** por petición del usuario; NO reintentar continuamente.
- Radio recomendado: 2500 metros; hasta 12 lugares con nombre.
- Debéis **redactar vosotros la consulta Overpass QL**. La documentación explica las expresiones `nwr`, los filtros por etiqueta `[...]`, el filtro espacial `around` y la instrucción `out center` para recuperar también centros de polígonos. Buscad un ejemplo en la documentación de Overpass y adaptadlo; no se facilita una consulta completa lista para pegar.
- Preguntas para diseñarla: ¿qué etiquetas varían con el tipo de turismo?, ¿cómo se insertan unas coordenadas validadas?, ¿qué ocurre si hay cero resultados?, ¿cómo limitáis las solicitudes a un servidor público?

**Adaptación por categorías (sin resolver):**

| Tipo seleccionado | Etiquetas OpenStreetMap candidatas |
|---|---|
| Cultural | `tourism=museum/attraction/gallery` o `historic=monument/castle/memorial` |
| Gastronómica | `amenity=restaurant/cafe/food_court` |
| Naturaleza | `leisure=park/garden` |
| Familiar | `tourism=attraction/zoo` o `leisure=park/playground` |

Estas categorías son aproximaciones a la disponibilidad de OSM; no garantizan horarios, accesibilidad o calidad. Debéis generar las condiciones según un **conjunto permitido de 4 tipos**, no insertando expresiones libres en Overpass QL.

El JSON devuelve `elements`. Para cada elemento hay que manejar:
- `tags.name`: si falta, descartarlo;
- `type=node`: coordenadas en `lat`, `lon`;
- `type=way` o `relation`: centro en `center.lat`, `center.lon` (porque pedimos `out center`);
- `tags`: sirve para deducir categoría.

Salida: lista de `{'nombre': str, 'categoria': str, 'lat': float, 'lon': float, 'fuente': 'OpenStreetMap', 'demo': False}`. Deduplicad por nombre cuando sea razonable. Si la respuesta está vacía, no se puede inventar una ruta real.

**Resiliencia:** el fichero `fixtures/puntos_demo.json` contiene 4 lugares ficticios. Si Overpass no responde, podéis usarlo para **demostrar la integración** y guardar `demo=true`. Es inaceptable presentar estos lugares como lugares verificados. Si se usa fixture, el resultado debe mostrar un aviso «DATOS DEMO» y también constar en la base de datos. También se admite mostrar al usuario «no hay lugares reales disponibles» y guardar el error.

## D. Cohere Chat v2 · contexto → propuesta

- Referencia: https://docs.cohere.com/v2/reference/chat
- URL: `https://api.cohere.com/v2/chat`, método `POST`.
- Autorización: `Authorization: Bearer <COHERE_API_KEY>` guardada en `.env` (no en Git).
- Modelo por defecto: `command-r7b-12-2024` (se configura con `COHERE_MODEL`).
- Consultad el contrato oficial de Chat v2 para estructurar los campos del modelo y los mensajes. El código de envío y de extracción del texto **no está resuelto**: investigad la estructura del JSON de respuesta y comprobad si hay contenido antes de acceder.
- El prompt lo redactáis vosotros y debe incluir preferencias, tipo, horas, meteorología, lugares recibidos y una restricción clara de **no inventar lugares, horarios ni eventos**. Mejor si explica qué hacer cuando llueve y cuándo los datos son insuficientes.
- Guardad evidencia de una versión inicial, de cómo respondió el modelo y de qué cambiasteis tras comprobar un problema. No basta con pedir a la IA «hazme un prompt» y copiarlo.
- La **clave no se guarda nunca**, ni en respuestas de API, ni en pantallas, ni en PostgreSQL, ni en commits o capturas de prompts.
- Si el docente no facilita una clave, `LLM_MODE=mock` permite ensayar el flujo sin un servicio generativo; no acredita el requisito de conexión real a Cohere.

## Contrato de la API PROPIA (obligatorio)

`POST /api/planificar`, `Content-Type: application/json`:

```json
{
  "ciudad": "Valencia",
  "tipo_turismo": "cultural",
  "duracion_horas": 4,
  "preferencias": "con niños, poco caminar"
}
```

Respuesta correcta orientativa (NO hay que copiar sus valores):

```json
{
  "solicitud_id": 17,
  "ciudad": "Valencia",
  "tipo_turismo": "cultural",
  "meteorologia": {"temperatura_c": 20, "precipitacion_mm": 0},
  "lugares": [{"nombre": "...", "lat": 0, "lon": 0}],
  "itinerario": "...",
  "modo_demo": false
}
```

Errores HTTP esperados: `400` para campo vacío o tipo inválido; `502`/`503` para problemas de proveedores, con mensaje útil; `200` en éxito. Nunca responder 200 con un error escondido. `GET /api/health` ya está programado. `GET /api/estadisticas` es obligatorio y debe mostrar analítica de PostgreSQL en JSON.

## Seguridad y límites mínimos

- `requests` siempre con `timeout`; `raise_for_status` o equivalente.
- Validar entrada: máximo 80 caracteres ciudad y 200 preferencias; tipos y duración entre valores permitidos.
- Escapar el HTML con Jinja2 normal; no usar `|safe` para texto libre del modelo.
- Nunca confiar en datos del LLM como si fueran hechos; el origen fiable de los lugares es OSM.
- Toda consulta SQL parametrizada. No concatenar entradas del usuario en SQL.
- Servidores externos: peticiones moderadas, no bucles de scraping.
- Citar Open-Meteo y © colaboradores OpenStreetMap en la interfaz (pie ya incluido).
