# Checklist de aceptación y auxilio técnico

## Docker / red

- `docker compose ps` → `db`, `web`, `jupyter` activos.
- `http://localhost:5000/api/health` → `db: ok`.
- En Docker, la base de datos es `db:5432`, no `localhost:5432`.
- Dentro de Jupyter, Flask está en `http://web:5000`.
- `http://localhost:8888` abre la sesión Jupyter.
- `db/init.sql` se aplica al **primer arranque de un volumen**. Cambiar el SQL no reconstruye automáticamente tablas existentes. `docker compose down -v` borra todos los datos de Postgres; evitarlo salvo que sea intencionado.

## Pruebas obligatorias del Jupyter

1. Consulta externa de ciudad y tiempo: imprimir nombre + coordenadas, temperatura y situación de lluvia. No usar valores fijos como si fueran reales.
2. `GET /api/health` y `POST /api/planificar` vía `requests` desde el **contenedor Jupyter** (no `localhost:5000`). Comprobar status, JSON y campos básicos.
3. PostgreSQL vía SQLAlchemy: `SELECT COUNT(*) FROM solicitudes` y `SELECT ciudad, tipo_turismo, estado ... LIMIT 5`.
4. Un caso con entrada no válida que devuelva `400` (por ejemplo, ciudad vacía) o un caso controlado de fallo externo.

## Verificaciones funcionales

- Usuario escribe «Valencia», elige cultural, 4 h y «con niños».
- Se geocodifica; se consulta el clima; se extraen lugares OSM con nombre y coordenadas.
- Cohere **recibe ese contexto** y devuelve una ruta sin lugares inventados; si está en mock se indica explícitamente.
- La UI muestra ruta y meteorología, y avisa de que los horarios no están verificados.
- El API propio devuelve JSON equivalente.
- PostgreSQL registra entrada, lugar, meteorología, prompt, resultado, fecha, estado y tiempo de ejecución.
- El dashboard obtiene total, nº por ciudad y 8 últimas peticiones de la DB, más al menos 1 gráfica con Matplotlib (PNG) y una tabla.
- Se han ejecutado >=5 peticiones de prueba repartidas entre al menos 2 ciudades y 2 tipos.
- Están enlazados 2 PR por autor con revisión real.
- Cada estudiante entrega `entrega/MEMORIA_IA_<NOMBRE>.md`, con registro de ayuda generativa y otras fuentes, decisiones propias, pruebas y vínculos a sus PR (o declaración de no uso).

## SQL de comprobación manual (solo lectura)

```sql
SELECT COUNT(*) FROM solicitudes;
SELECT id, fecha, ciudad, tipo_turismo, estado
FROM solicitudes ORDER BY fecha DESC LIMIT 5;
SELECT ciudad, COUNT(*) AS peticiones
FROM solicitudes GROUP BY ciudad ORDER BY peticiones DESC;
```

## Problemas y pistas

| Síntoma | Posible causa | Qué comprobar |
|---|---|---|
| Web arriba, error DB | `localhost` dentro de contenedor o variable errónea | `DATABASE_URL`, nombre de servicio `db` |
| Overpass 429/502/504 | Servidor público saturado | timeout, no repetir en bucle, fixture claramente etiquetada |
| Geocoding devuelve lista vacía | Nombre no reconocido o filtros demasiado estrictos | `results` vacío, `countryCode`, nombre |
| Cohere 401 | Clave inexistente/errónea | `.env`, reiniciar `web`, clave docente |
| Cohere 429 | Límite de evaluación compartida | probar `mock`, no lanzar ráfagas |
| No aparecen tablas nuevas | `init.sql` solo se aplica al inicio del volumen | inspeccionar schema; no borrar volumen sin decidirlo |
| Jupyter no ve web | URL equivocada | `http://web:5000`, no `localhost` |
| La UI muestra datos demo como reales | Error de honestidad de los datos | marcar `demo=true` y aviso visible |

## Comandos útiles

```bash
docker compose logs -f web
docker compose exec web python -m pytest -q
docker compose exec db psql -U citypilot -d citypilot
docker compose ps
docker compose down          # conserva volumen
docker compose down -v       # ¡BORRA BD! solamente si se desea reiniciar
```
