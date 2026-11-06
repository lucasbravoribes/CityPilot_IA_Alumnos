# Trabajo colaborativo — 2 Pull Requests por estudiante (obligatorio)

La evidencia no son solo commits. **Cada integrante debe abrir 2 Pull Requests propios**, proponer cambios en una rama y obtener revisión del compañero antes de fusionar a `main`.

## Roles orientativos para equipo de 2

| Persona | PR 1 (bloque de datos) | PR 2 (bloque de aplicación) |
|---|---|---|
| A | Geocoding + meteorología; test con respuesta simulada | Formulario HTML + interfaz de resultados + llamadas a un orquestador compartido |
| B | Overpass + normalización de POI; test con fixture | PostgreSQL + consultas de estadísticas + dashboard |

La **orquestación** y la **llamada real a Cohere** se integran de forma conjunta durante la sesión; pueden repartirse en los PR ya previstos (por ejemplo A: Cohere, B: DB) sin crear PRs extra si la organización queda clara. Jupyter se hace conjuntamente y se integra en los PRs correspondientes. Si sois 3, cada persona debe abrir sus 2 PRs (mínimo 6).

## Flujo sugerido

1. Acordad quién se ocupa de cada archivo y la forma de los diccionarios de salida, antes de programar.
2. Cada persona crea su rama desde `main` (`feature/geoclima-a`, `feature/lugares-b`, etc.) y trabaja en archivos distintos.
3. Commit de cambios pequeños; `push` de la rama; abrir PR con descripción, pruebas realizadas y riesgos.
4. El compañero revisa un PR (comentario concreto, no solo un pulgar arriba), solicita correcciones si procede y aprueba. Merge a `main`.
5. `pull` de `main`, crear una segunda rama nueva y repetir. No se aceptan 2 PR hechos por la misma persona en nombre de su compañero.

**Problema típico:** los dos PR modifican `main.py` o `requirements.txt`. Acordad cambios antes o fusionad en serie. Si hay conflicto, resolverlo y dejar constancia de la resolución.

## Mini-plantilla de descripción de PR

```
¿Qué aporta este PR?
¿Cómo lo he probado?
¿Qué queda pendiente o puede fallar?
¿Qué debe revisar mi compañero?
```

## Evidencias finales

- En el README del repositorio, sección «Equipo y colaboración»: nombres, reparto y **enlaces a los 4 PR mínimos**, con autor y revisor.
- Al menos **un comentario de revisión útil** en cada PR (errores, propuesta, prueba, documentación).
- El historial debe permitir ver dos ciclos de PR por persona, fusionados en `main`.
- Los commits directos a `main` no cuentan como PR.
- `.env` y claves fuera del repositorio, incluso si es privado.

## Semáforo amarillo: trazabilidad por autor

Cada persona debe poder explicar sus dos PR y señalar en su **memoria individual** dónde recibió asistencia de IA o empleó fuentes externas. Si un fragmento importante se creó con asistencia, la descripción de PR puede indicarlo y enlazar a la entrada correspondiente de la memoria. **No se aceptan PR cosméticos para ocultar quién implementó el código.** El histórico, las revisiones y las pruebas deben ser coherentes con el relato individual. Consultad `docs/SEMAFORO_AMARILLO_Y_MEMORIA.md`.
