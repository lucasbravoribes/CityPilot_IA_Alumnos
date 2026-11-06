# Semáforo amarillo — Reglas y memoria de utilización de IA

## Qué significa el semáforo amarillo en este taller

**Se permite utilizar herramientas de IA como asistencia**, siempre que el aprendizaje, las decisiones técnicas y las contribuciones individuales sean verificables. No es una actividad de «IA prohibida», ni se penaliza pedir ayuda. El objetivo es que sepáis explicar vuestro trabajo y reconocer honestamente de dónde sale cada parte.

**Usos aceptables, si se declaran:** preguntar por un error de `requests`, pedir una explicación de `JSONB` o de una condición Overpass, solicitar alternativas, revisar un test, recibir sugerencias sobre el prompt, generar un ejemplo aislado y adaptarlo tras probarlo, consultar código en documentación o GitHub y citarlo. El código finalmente incorporado debe estar **revisado, probado y comprendido** por su autor.

**Usos incompatibles con la actividad:** pedir a una IA o a otra persona que haga el proyecto entero y entregarlo sin trabajo propio; copiar módulos, formularios, tests o prompts generados y ocultarlo; inventar intentos o fuentes; atribuirse commits o PR ajenos; presentar pruebas que no se han ejecutado; afirmar que se creó algo manualmente cuando fue copiado directamente. Copiar código de un repositorio público sin atribución también se debe declarar, aunque no sea IA.

**No se exige programar todo sin ayuda. Se exige aprendizaje y honestidad.** La memoria debe reflejar usos sustantivos, no cada pregunta trivial. Registrar los intentos conforme trabajáis es más rápido que reconstruirlos al final.

## Entrega OBLIGATORIA: una memoria por cada estudiante

1. Cada integrante entrega `entrega/MEMORIA_IA_<NOMBRE>.md` utilizando la plantilla facilitada y sustituyendo los textos entre corchetes.
2. Cada memoria incluye una identificación, qué partes implementó personalmente, herramientas y modelos usados, registro cronológico de interacciones relevantes (también intentos fallidos), código o material externo reutilizado y enlaces verificables a commits/PR.
3. En cada entrada relevante anotad **tarea → instrucción/prompt o descripción reproducible → respuesta recibida → qué aceptasteis, cambiasteis o descartasteis → cómo lo probasteis**.
4. Si usasteis varias versiones del prompt del planificador, describid al menos una secuencia **V1 → resultado/limitación → cambio → V2**. Indicad cuándo el modelo inventó lugares o ignoró una preferencia, si ocurrió. No hay que inventar fallos para aparentar trabajo.
5. Declarad también código tomado o adaptado de documentaciones, Stack Overflow, GitHub, apuntes y de un compañero; proporcionad URL o referencia y explicad qué cambiasteis.
6. Si NO utilizasteis IA, entregad igualmente la memoria indicando «No he utilizado IA generativa», fuentes no generativas consultadas y contribuciones propias, con PR y pruebas.
7. No pongáis claves API, tokens, contraseñas, datos privados ni encabezados de autenticación. Si las capturas o conversaciones incluyen secretos, redactadlos antes de entregar.

**Ejemplo breve de cómo registrar el proceso (ilustrativo; no es un prompt listo para la actividad):**

- *Tarea:* interpretar un error HTTP 429 de Overpass.
- *Asistencia:* pregunté a un chatbot qué significa el 429 y cómo diferenciarlo del caso sin resultados. Conservé una captura sin credenciales.
- *Respuesta y decisión:* sugirió reintentar indefinidamente; lo descarté porque es un servidor comunitario. Preferí mostrar error de proveedor y usar fixture DEMO solo para pruebas.
- *Trabajo propio y evidencia:* incorporé tratamiento del error en `api_clients.py`, PR #7, y comprobé en test `test_overpass_429` que se mostraba un mensaje útil.

Una memoria que diga «he usado ChatGPT para varias dudas» sin indicar tareas, salidas, decisiones ni pruebas **no es suficiente**. Una colección de 60 capturas sin explicación tampoco.

## Cómo se evalúa y qué consecuencias tiene falsear la memoria

La memoria forma parte de la rúbrica con **2 de los 10 puntos** de la actividad. El profesor valora cobertura y precisión del registro, reflexión crítica, evidencias contrastables y atribución de las contribuciones. Tener más consultas a IA no implica mejor ni peor nota; importa que el registro sea fiel.

**Adicionalmente, una ocultación o falsedad relevante y fundamentada puede implicar una reducción de hasta el 30 % de la calificación final de ESTA actividad**, con independencia de los puntos que se pierdan por una memoria deficiente. Esta reducción **no es automática** por usar mucha IA ni por un resultado con «estilo IA». Antes de aplicarla, se contrastarán hechos (coherencia entre memoria, repositorio, PR, código, pruebas y explicaciones), se pedirá aclaración al estudiante y se valorará la gravedad. Indicios o detectores automáticos por sí solos no demuestran autoría.

Ejemplos de circunstancias relevantes: afirmar que se escribió un módulo manualmente cuando se copió íntegro de una respuesta generativa y se ocultó; presentar PR sin contribución personal; inventar capturas o ensayos; no poder justificar un bloque crítico mientras se niega asistencia que consta en el trabajo. No se penaliza reconocer «esta función se creó con ayuda, la adapté, la probé y puedo explicar cómo funciona».

**Cálculo:** primero se aplica la rúbrica y el bonus, con nota máxima 10; después, en su caso, una reducción motivada entre 0 % y 30 % sobre esa nota de la actividad. Por ejemplo, 8,0 puntos y reducción motivada del 20 % → 6,4 puntos. **No significa perder el 30 % de la nota de toda la asignatura.** La falta de memoria se valora como incumplimiento del criterio de 2 puntos; no implica por sí sola una acusación de falsedad.

## Control rápido de calidad antes de entregar

- ¿Cada integrante tiene su propio documento y sus 2 PR enlazados?
- ¿Se indican herramientas/modelos (o explícitamente ausencia de uso)?
- ¿Se han descrito los usos relevantes, con al menos un ejemplo de decisión técnica?
- ¿Están registrados los prompts empleados para producir o revisar el prompt del planificador y el resultado de los ensayos?
- ¿Se señalan los fragmentos adaptados de IA, GitHub u otras fuentes y las modificaciones hechas?
- ¿Pueden localizarse pruebas, commits y revisiones que respalden lo contado?
- ¿Se han excluido secretos y datos personales?
