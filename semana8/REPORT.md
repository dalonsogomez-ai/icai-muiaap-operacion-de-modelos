# Informe de la práctica 8 — Chatbot con FastAPI, LLM y modelo

## Leyenda utilizada

- `->` Objetivo o problema que quiero resolver.
- `~>` Decisión o cambio realizado y su justificación.
- `>` Acción técnica ejecutada.
- `>>` Evidencia verificable: archivo, salida o comprobación.
- `=>` Resultado obtenido y estado de verificación.

## Objetivo y preparación

`->` He construido el backend que conecta el chat de Streamlit con el modelo de impago mediante una tool. He seguido el [MD del profesor](modules/08-chatbot-llm-api/exercises/01-chatbot-riesgo-impago/problem/ENUNCIADO_ALUMNOS.md) y el [Assignment 8.2](../assignments/semana08_clase02_assignment.pdf), que coinciden en el alcance.

`>` He revisado las entregas de S1 a S7: trazabilidad y evidencia real en S1, entorno con uv en S2, contratos e inferencia separados en S3, carga y validación del artefacto en S4, consumo desde Streamlit en S5, estado y errores en S6 y cliente HTTP en S7. Conservo los comentarios breves en español y en primera persona, explicando las decisiones que afectan al resultado.

`~>` El checkout principal tenía S8 como marcador. He utilizado la copia distribuida del material docente en Descargas y he creado el worktree independiente `icai-semana8-tareas`, rama `tareas-semana8`, desde `23153b5` de la entrega S7. Así conservo el trabajo previo y la estructura que proporciona el profesor.

## Requisitos y comprobaciones

| Requisito | Implementación | Evidencia |
| --- | --- | --- |
| Seis variables, rangos, campos extra y antigüedad | `app/schemas/prestamo.py` | Tests originales y casos límite |
| Joblib cargado una vez, orden de features y umbrales | `app/services/modelo.py` | Tests del modelo, fronteras 0,2 y 0,5 |
| Schema de la tool generado desde Pydantic | `definir_tool()` | Igualdad con `model_json_schema()` |
| Resultado con ok tanto en éxito como en error | `ejecutar_tool()` | JSON roto, campos extra, entrada inválida y fallo de inferencia |
| Historial system → assistant → tool y máximo de vueltas | `responder()` | Recuperación, IDs de tools y exactamente cuatro llamadas |
| POST /predict y /chat con Depends(get_llm) | `app/routers/` | TestClient y peticiones HTTP a Uvicorn |
| Chatbot completo con simulador | Frontend y cliente docentes sin cambios | Interacción visual en VS Code |
| Entrega reproducible y enlace final | README, lockfile, modelo y rama local | Publicación pendiente de autorización |

Las rutas de código de la tabla son relativas a [problem/](modules/08-chatbot-llm-api/exercises/01-chatbot-riesgo-impago/problem/).

## Decisiones y relación con clase

`~>` Declaro `edad` antes de `antiguedad_laboral_anios` y uso `field_validator` con `@classmethod` y `ValidationInfo.data` para comprobar `antigüedad <= edad - 16`. Si la edad ya falla, no accedo a una clave inexistente. Uso `ConfigDict(extra="forbid")` y rechazo valores no finitos antes de inferir.

`>>` En la [clase del 23 de octubre](https://notes.granola.ai/d/7ae9b137-f671-47e3-8fdf-66260eb36c25), los tramos 36:45–40:20 y 51:48–53:10 trabajan los campos, el rechazo de extras y el acceso a `info.data`. La [documentación de Pydantic](https://docs.pydantic.dev/latest/concepts/validators/#validation-data) aclara que ese acceso contiene los campos ya validados y depende del orden de declaración.

`~>` Genero `parameters` con `PrestamoEntrada.model_json_schema()`, como se explica en el tramo 59:52–64:07 de esa clase. Evito mantener otra lista de campos para la tool. La regla entre edad y antigüedad se comprueba en Python; incluyo su descripción para el LLM, pero el JSON Schema no sustituye al validator.

`~>` Cargo el modelo al importar `modelo.py`, como indica el TODO del starter: una vez por proceso de Python, sin recargarlo por petición. No cambio `main.py` para introducir lifespan. La clase comenta ambas formas de carga alrededor del minuto 65. Conservo `VARIABLES` para construir las seis posiciones y valido la salida con `PrediccionSalida`.

`~>` En `/predict` dejo que FastAPI devuelva 422 cuando el cuerpo no cumple el contrato. En la tool devuelvo un diccionario con `ok=False` y el error para permitir que el LLM se corrija. Capturo los errores inesperados en esa frontera con un mensaje genérico; no expongo detalles internos de un fallo de inferencia.

`~>` El orquestador conserva cada mensaje del asistente y devuelve un mensaje `tool` por llamada con su `tool_call_id`. No modifica la conversación original. Si hay varias tools en una vuelta, procesa sus resultados; el contrato del frontend tiene una única `herramienta`, por lo que muestra la última. `MAX_VUELTAS=4` cuenta llamadas al LLM, incluida su respuesta final.

`~>` Uso funciones síncronas en las rutas porque el cliente y la inferencia del starter son síncronos. `Depends(get_llm)` permite usar el cliente docente o sustituirlo en los tests. `response_model` declara y valida la salida; son los mecanismos documentados de [dependencias](https://fastapi.tiangolo.com/tutorial/dependencies/) y [response models](https://fastapi.tiangolo.com/tutorial/response-model/) de FastAPI.

## Modelo y entorno

`>` La primera ejecución pasó 31 tests, pero mostró `InconsistentVersionWarning`: el Joblib original procedía de scikit-learn 1.7.2 y el entorno resuelto usa 1.9.1. Conservé el original en `problem/.tmp/modelo_impago_original.joblib`, fuera de Git, y ejecuté `uv run python scripts/entrenar_modelo.py`, tal como permite el assignment ante incompatibilidad de versión.

`>>` El [registro del artefacto y entorno](entrega/evidencias/entorno-modelo.json) guarda ambos SHA-256 y las versiones. El script docente, sin cambios, genera 3000 filas sintéticas con semilla 7 y entrena `StandardScaler + LogisticRegression`. Las clases comprobadas son `[0, 1]` y el modelo recibe seis features; por eso la columna 1 de `predict_proba` es la de impago.

`~>` Conservo `pyproject.toml` con dependencias sin versiones y sin añadir una versión fija de Python. `uv.lock` registra la resolución utilizada, ejecutada con Python 3.13.13. El aviso de uv sobre `requires-python` corresponde a esa configuración docente. Incluyo el Joblib regenerado para que los tests funcionen tras clonar.

## Ejecución y resultados

`>` He realizado la preparación, edición y ejecución desde la terminal integrada de Visual Studio Code usando Ordenador. El [README](README.md) contiene los comandos de instalación, tests y arranque de Uvicorn y Streamlit. He seleccionado en el editor el intérprete del entorno `.venv` del ejercicio.

`>>` [Pytest](entrega/evidencias/pytest.txt): **31 tests originales en verde**, sin modificar la suite. Permanece un `UserWarning` de Pydantic sobre `ReadOnly` al probar el cliente LiteLLM; no he silenciado el aviso. Los tests del cliente simulan sus respuestas y no necesitan un proveedor externo.

`>>` [Casos límite](entrega/evidencias/casos-limite.txt): compruebo los umbrales exactos, la antigüedad en el límite, valores no finitos, entradas que no deben llamar al modelo, fallo controlado de inferencia, schema idéntico a Pydantic, máximo exacto de cuatro vueltas y dos tools con IDs distintos.

`>>` [HTTP real](entrega/evidencias/http-real.txt): Uvicorn responde 200 en `/health`, 200 en una predicción válida y 422 ante edad inválida o campos extra. `/chat` devuelve la predicción con la tool, pide los campos ausentes y rechaza una conversación vacía con 422. Conservo el [OpenAPI generado](entrega/evidencias/openapi.json).

`=>` Para edad 30, ingresos 2500, importe 12000, plazo 36, antigüedad 5 e impagos 0, obtengo probabilidad `0.16371773677464993` y decisión `aprobar`. Streamlit la presenta redondeada a `16.4 %`.

`>>` He probado el frontend real en el navegador integrado de VS Code: backend conectado, envío del ejemplo completo, despliegue de los seis argumentos y del resultado de la tool, conversación en dos turnos con los campos que faltan y rechazo de antigüedad 15 para edad 20. El registro de estas observaciones está en [ejecucion-visual.md](entrega/evidencias/ejecucion-visual.md). El enunciado no exige capturas de pantalla.

`>>` He repetido `uv sync --locked` y `uv run --locked pytest` en una copia limpia obtenida con `git archive` del commit `b818f78`, sin reutilizar el entorno ni los ficheros ignorados del worktree. Resultado: **31 passed, 1 warning in 9.51s**. El modelo está incluido en Git. Registro completo: [checkout-limpio.txt](entrega/evidencias/checkout-limpio.txt).

## Alcance y límites

`~>` Conservo sin cambios `llm.py`, el frontend, los contratos del chat, los tests y el script de entrenamiento. Docker es un extra opcional del assignment. El MD y el PDF concretos no exigen ngrok, aunque el roadmap antiguo lo mencione.

`>>` El simulador docente usa expresiones regulares; esta ejecución comprueba el flujo y los contratos, no la comprensión de lenguaje natural de un LLM real. No he configurado un proveedor externo ni realizado llamadas de pago. El frontend conserva los avisos de deprecación de `use_container_width` del material original.

`>>` El modelo es sintético y los umbrales vienen impuestos por el ejercicio. Esta práctica no evalúa discriminación ni calibración para solicitudes reales: el resultado demuestra integración, no validez para conceder préstamos.

`=>` Backend implementado y comprobado localmente en `tareas-semana8`. La publicación en el fork requiere la autorización indicada por el AGENTS.md del usuario; no doy por existente una rama remota todavía.
