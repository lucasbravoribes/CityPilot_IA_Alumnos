# CityPilot IA — ¿Qué hacemos hoy?

**Taller evaluable · 150 minutos · equipos de 2 (excepcionalmente 3) · SEMÁFORO AMARILLO · memoria IA individual obligatoria.**

Una aplicación real de rutas urbanas: formulario web → geocodificación → meteorología → lugares abiertos → Cohere → itinerario → PostgreSQL → dashboard. No se utiliza JavaScript: HTML, CSS y Flask bastan.

> **Este es un proyecto BASE, deliberadamente incompleto.** Docker, las dependencias, el esquema SQL, las vistas vacías y la estructura ya están preparados. Tenéis que implementar el flujo de negocio, el formulario, las consultas externas, el prompt, la persistencia y la analítica. Los archivos identifican los puntos de trabajo mediante `TODO(ALUMNADO)`.

## Primeros 5 minutos

1. Descomprimid la carpeta, cread un repositorio GitHub **privado o público sin credenciales**, e invitad al otro integrante como colaborador.
2. Copiad `.env.example` a `.env`. `LLM_MODE=mock` permite empezar sin clave. Para el resultado real, usad `LLM_MODE=cohere` y **una clave proporcionada por el docente** en `COHERE_API_KEY`. No se sube a Git.
3. Ejecutad desde la raíz:

   ```bash
   docker compose up --build -d
   docker compose ps
   ```

4. Abrir: http://localhost:5000 (web), http://localhost:5000/analitica (panel), http://localhost:5000/api/health (salud), http://localhost:8888 (Jupyter).
5. Los formularios y las rutas de planificación están **sin implementar a propósito**. Un mensaje 501 significa tarea pendiente, no que Docker esté roto.

Si 5000, 5433 u 8888 están ocupados, cambiarlos en `.env` (`WEB_PORT`, `PG_PORT`, `JUPYTER_PORT`).

## Archivos clave

- `GUIA_ALUMNADO.pdf` / `.md`: enunciado, fases, pruebas, rúbrica y entregables.
- `docs/APIS_Y_CONTRATOS.md`: URLs, parámetros, salidas, funciones y fallos esperados.
- `docs/TAREAS_Y_CRITERIOS.md`: qué implementar y cómo comprobar cada función, **sin dar el código**.
- `docs/SEMAFORO_AMARILLO_Y_MEMORIA.md`: reglas detalladas de uso transparente de IA y posible reducción hasta 30 % por falseamiento acreditado.
- `entrega/MEMORIA_IA_PLANTILLA.md`: plantilla a copiar, una memoria por estudiante, con prompts, ayudas, errores, pruebas y PR.
- `docs/GIT_Y_PRS.md`: organización de GitHub y **2 PR por cada integrante**.
- `docs/COMPROBACIONES.md`: checklist técnico y consultas SQL de apoyo.
- `web/app/`: esqueleto Flask y funciones que tendréis que implementar.
- `web/app/templates/`: plantillas HTML **sin formularios terminados**.
- `db/init.sql`: tabla ya definida para concentrarse en integración.
- `notebooks/01_validacion.ipynb`: comprobación de servicios con Jupyter (celdas incompletas).
- `fixtures/`: respuestas simuladas para probar contratos y recuperar el taller si falla un proveedor.

## Qué NO proporciona este paquete

No contiene el prompt listo, la consulta Overpass QL terminada, las funciones de consumo de APIs, el orquestador de peticiones, el formulario, la escritura SQL, las consultas de analítica ni el dashboard terminado. Eso es exactamente lo que se evalúa. La **memoria individual de IA** aporta 2/10 puntos, y la ocultación o falsedad contrastada puede reducir adicionalmente hasta un 30 % la nota de esta actividad.

**Fuentes y atribución:** Open-Meteo (https://open-meteo.com), OpenStreetMap/Overpass (https://www.openstreetmap.org/copyright), Cohere (https://docs.cohere.com). Open-Meteo es libre para uso no comercial; respetad atribución y los límites de los servicios públicos.
