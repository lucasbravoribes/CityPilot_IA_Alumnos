# Memoria individual de utilización de IA — CityPilot IA

> Actividad de **semáforo amarillo**. Esta memoria describe con precisión la ayuda recibida. No contiene claves ni secretos.

## 1. Autoría y aportación individual

- Estudiante: Jordi Aguado (usuario GitHub: `jordiagdo-debug`)
- Equipo: Jordi, Lucas Bravo (`lucasbravoribes`), Alessandro Europea, Javier Garrido
- Repositorio GitHub: https://github.com/lucasbravoribes/CityPilot_IA_Alumnos
- Mi parte en el reparto del grupo: **base de datos (PostgreSQL) y panel de analítica**.
- Mis dos PR, con revisión cruzada (revisor: Lucas Bravo):
  - **PR 1** — rama [`feature/db-guardar`](https://github.com/lucasbravoribes/CityPilot_IA_Alumnos/tree/feature/db-guardar): 
  `guardar_solicitud`.
  - **PR 2** — rama [`feature/db-analitica`](https://github.com/lucasbravoribes/CityPilot_IA_Alumnos/tree/feature/db-analitica): PR  — estadísticas, panel y gráfica.
- Archivos y funciones de mi parte:
  - `web/app/db.py`: `_parametros_insert`, `guardar_solicitud`, `obtener_estadisticas`, `obtener_ultimas_solicitudes`.
  - `web/app/grafico.py` (nuevo): `generar_grafico_png`.
  - `web/app/templates/analitica.html`.
  - `web/app/main.py`: rutas `/analitica`, `/analitica/grafico.png`, `/api/estadisticas`.
  - `web/tests/test_db_guardar.py` y `web/tests/test_db_analitica.py`.
- **Importante (honestidad):** el código de estos archivos **lo propuso Claude** y yo lo incorporé, lo ejecuté, lo probé y corregí los fallos de integración que aparecieron. No lo escribí desde cero. Lo especifico en las secciones 3 y 5.
- Pruebas que ejecuté personalmente:
  - `docker compose exec web python prueba_db.py` (script temporal, no incluido en los PR): insertó filas y devolvió ids 1 y 2.
  - `docker compose exec db psql ... SELECT ...`: comprobé que `meteorologia` y `lugares` se guardan como JSONB.
  - `docker compose exec web python -m pytest -q tests`: **10 passed**; mis tests: `tests/test_db_guardar.py` y `tests/test_db_analitica.py` → **3 passed**.
  - Panel real en http://localhost:5000/analitica con datos de PostgreSQL (captura: [RUTA, p. ej. `entrega/captura_panel.png`]).

## 2. Herramientas y fuentes usadas

| Herramienta o fuente | Modelo/versión, si se conoce | Finalidad | ¿Se incorporó código o texto? |
|---|---|---|---|
| Claude (claude.ai) | Claude Sonnet 5.5 | Explicar el flujo de trabajo, guiar paso a paso, proponercódigo alternativo al escrito con corrección de fallos de mi parte, depurar errores, redactar plantillas de PR| **Sí**: funciones de `db.py`, `grafico.py`, `analitica.html`, rutas de `main.py`, 3 tests |
| Documentación de la guía del taller (`docs/APIS_Y_CONTRATOS.md`, `docs/TAREAS_Y_CRITERIOS.md`, `docs/GIT_Y_PRS.md`) | — | Contrato de columnas y requisitos | Estructura de la tabla y requisitos |
| GitHub Desktop / Docker Desktop / VS Code | — | Ramas, commits, PR, contenedores | No aplica |

## 3. Registro cronológico de uso RELEVANTE de IA

### Interacción 1 — 06/11/2026, ~09:00–09:30. Entender la tarea, el reparto y el flujo de Git

- **Qué respondió:** resumió el flujo (formulario → orquestador → APIs → BD → panel), propuso un reparto en 4, 2 ramas por persona y un círculo de revisión cruzada.
- **Qué hice yo:** seguí el reparto de mi parte (BD y analítica) y partí mi trabajo en dos ramas, una por PR.
- **Resultado y verificación:** ramas `feature/db-guardar` y `feature/db-analitica` en el repositorio.
- **Evidencia:** enlaces a las ramas (sección 1).

### Interacción 2 — ~09:42. Error: el contenedor `web` no arrancaba

- **Qué intentaba resolver:** `service "web" is not running` al probar.
- **Prompt:** pegué la salida de `docker compose ps -a` y `docker compose logs web`.
- **Qué respondió Claude:** el log mostraba `from CityPilot_IA_Alumnos.web.app.db import ping_db` en la línea 3 de `main.py` (un import automático de VS Code); indicó cambiarlo a un import válido dentro del contenedor.
- **Qué hice yo:** corregí la línea, reinicié `web` y la prueba funcionó. Decidí no meter ese arreglo en mi PR 1 (era de `main.py`, que no era mi parte) y avisé al grupo.
- **Resultado y verificación:** `web` volvió a estar *Up* y `prueba_db.py` imprimió el id.
- **Evidencia:** log de `docker compose logs web`. Más tarde otro compañero dejó el import como `from .db import ping_db`.

### Interacción 3 — ~09:56. Tests: `test_smoke.py` roto

- **Qué intentaba resolver:** `pytest` fallaba al recoger `test_smoke.py` (`ModuleNotFoundError` y después `IndexError: 3` por `parents[3]`).
- **Qué respondió Claude:** el mismo problema de imports automáticos en el fichero de tests; propuso restaurar el encabezado del archivo (`parents[1]` y `from app.main import create_app`).
- **Qué hice yo:** reemplacé el archivo, ejecuté `pytest` y comprobé **10 passed**. No incluí `test_smoke.py` en mis commits.
- **Resultado y verificación:** `10 passed` (captura de terminal).
- **Evidencia:** `web/tests/test_smoke.py` en mi copia local; tests de la sección 1.

### Interacción 6 — ~10:00–10:30. Estadísticas, panel y gráfica (PR 2)

- **Qué intentaba resolver:** `obtener_estadisticas`, `obtener_ultimas_solicitudes` (8 filas), panel con métricas reales, PNG con Matplotlib y `/api/estadisticas`.
- **Qué propuso Claude:** consultas SQL con `COUNT(*)`, `COUNT(DISTINCT ciudad)`, `COUNT(*) FILTER (WHERE estado='error')`, `GROUP BY ... ORDER BY ... LIMIT`, `ORDER BY fecha DESC, id DESC LIMIT :limite` (parámetro, sin concatenar); `grafico.py` con `Figure()` (sin `pyplot`) escribiendo a `BytesIO`; plantilla Jinja con escape automático; rutas con `try/except` para no mostrar trazas y `Cache-Control: no-store` en la imagen. Dos tests propios (PNG con y sin datos; el panel y la API degradan con mensaje si falla la BD).
- **Qué hice yo:** incorporé los archivos, inserté filas de prueba con un script temporal, abrí `/analitica`, `/analitica/grafico.png` y `/api/estadisticas`, y ejecuté los tests.
- **Resultado y verificación:** el panel mostró métricas reales de PostgreSQL (2 peticiones, 2 ciudades, 0 errores) y las dos gráficas de barras; los tests pasaron. [AÑADE aquí lo que viste tras añadir más filas y refrescar.]
- **Evidencia:** PR `web/tests/test_db_analitica.py`


### Interacción 7 — ~10:24. Error de sangría en `main.py`

- **Qué intentaba resolver:** revisar mi edición de `main.py` antes de ejecutarla.
- **Prompt:** pegué el contenido de `main.py`.
- **Qué respondió Claude:** detectó que `@app.get("/analitica")` tenía 7 espacios en lugar de 4, lo que habría producido `IndentationError`.
- **Qué hice yo:** corregí la sangría, reinicié `web` y el panel cargó.
- **Evidencia:** `web/app/main.py` en la rama `feature/db-analitica`.

### Interacción 8 — ~10:40. Conflicto de Git en `main.py`

- **Qué intentaba resolver:** conflicto entre mi rama y `main` (mis compañeros habían fusionado `/planificar` y `/api/planificar` en el mismo archivo).
- **Prompt:** pegué el archivo con los marcadores `<<<<<<<`, `=======`, `>>>>>>>`.
- **Qué respondió Claude:** conservar ambas partes: imports de los dos lados, las rutas de planificar de mis compañeros sin tocarlas y mis tres rutas de analítica ("Accept Current Change" en el bloque inferior).
- **Qué hice yo:** resolví el conflicto; la primera vez quedó un resto (`>>>>>>> main`) que GitHub Desktop rechazaba; lo eliminé, confirmé con Ctrl+F que no quedaban marcadores y completé el merge.
- **Resultado y verificación:** GitHub Desktop me dejó continuar; probé `/analitica` tras el merge.
- **Evidencia:** commit de merge en `feature/db-analitica`.


## 4. Evolución del prompt de itinerarios

No aplica: no he trabajado en `llm.py` ni en el prompt del planificador.

## 5. Código o materiales externos incorporados

| Archivo/líneas aproximadas | Origen | ¿Copiado o adaptado? | ¿Qué cambio/validación hice? |
|---|---|---|---|
| `web/app/db.py` — `_parametros_insert`, `guardar_solicitud` | Propuesta de Claude | Copiado de la propuesta | Probado con `psql` e inserciones reales; test `test_db_guardar.py` |
| `web/app/db.py` — `obtener_estadisticas`, `obtener_ultimas_solicitudes` | Propuesta de Claude | Copiado de la propuesta | Probadas con filas reales; panel y `/api/estadisticas` |
| `web/app/grafico.py` | Propuesta de Claude | Copiado de la propuesta | Probado en el navegador (`/analitica/grafico.png`) y con test |
| `web/app/templates/analitica.html` | Propuesta de Claude | Copiado de la propuesta | Probado con datos reales |
| `web/app/main.py` — 3 rutas de analítica | Propuesta de Claude | Copiado; corregí la sangría y resolví el conflicto | Probado; los tests de `/analitica` pasan |
| `web/tests/test_db_guardar.py`, `web/tests/test_db_analitica.py` | Propuesta de Claude | Copiado de la propuesta | Ejecutados: 3 passed |
| Contrato de columnas de `solicitudes` | `db/init.sql` y docstring de la guía | Usado como referencia | Comprobado con `\d solicitudes` |

## 6. Balance personal

- **Dos decisiones técnicas que tomé yo:**  dejar `main.py` y `test_smoke.py` fuera del PR 1 para no mezclar arreglos ajenos; resolver el conflicto conservando las rutas de mis compañeros y las mías
- **Un error o solución que descarté:** el `import` automático de VS Code que rompía el contenedor, y lo que aprendiste de ello.
- **Qué código puedo explicar y demostrar:**  por qué `:parametros` evita inyección SQL, qué hace `CAST(... AS jsonb)`, `engine.begin()` (commit/rollback), `COUNT ... FILTER`, `Figure()` + `BytesIO`, y por qué la imagen lleva `Cache-Control: no-store`.
- **Qué sigue pendiente o limitado:** el contador de errores solo cuenta `estado = 'error'`, así que el orquestador debe guardar `ok`/`error`; el panel no tiene caché ni paginación; las pruebas de SQL son manuales (los tests automáticos no usan una base de datos real).

**Declaración:** Confirmo que la memoria describe fielmente mis fuentes, la asistencia recibida, los cambios que introduje y mi aportación personal. Jordi Aguado, 06/11/2026.
