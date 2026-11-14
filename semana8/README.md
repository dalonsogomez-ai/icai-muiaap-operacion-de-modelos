# Semana 8 - Chatbot con LLM, FastAPI y un modelo

La práctica de la semana construye el backend de un chatbot de solicitudes de
préstamo: una API FastAPI recibe la conversación, un LLM decide cuándo llamar a
una tool y la tool valida los datos con Pydantic y ejecuta el modelo joblib.
El frontend en Streamlit y el cliente del LLM (LiteLLM) vienen hechos.

## Acceso al material

[Abrir el módulo 08-chatbot-llm-api](modules/08-chatbot-llm-api/README.md)

Assignment en PDF: [Assignment 8.2](../assignments/semana08_clase02_assignment.pdf)

**Requisitos:** `uv`. No hace falta fijar versión de Python.

## Mi entrega

He completado los cinco archivos del backend del enunciado. Las decisiones y
los resultados están en [REPORT.md](REPORT.md).

Desde la raíz del repositorio:

~~~bash
cd semana8/modules/08-chatbot-llm-api/exercises/01-chatbot-riesgo-impago/problem
uv sync
uv run pytest
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
~~~

En otra terminal, desde la misma carpeta:

~~~bash
uv run streamlit run frontend/app.py --server.address 127.0.0.1
~~~

Abro el frontend en http://127.0.0.1:8501 y Swagger en http://127.0.0.1:8000/docs.
Sin LLM_MODEL se utiliza el simulador docente. Si había un proveedor externo
configurado, uso unset LLM_MODEL antes de arrancar para probar sin coste.

Conservo las dependencias sin versiones en pyproject.toml, como pide el profesor;
uv.lock registra la resolución utilizada. No añado .python-version.
Incluyo el modelo regenerado con el script docente. Si un entorno distinto
produce una incompatibilidad de scikit-learn, ejecuto desde problem:

~~~bash
uv run python scripts/entrenar_modelo.py
~~~

Las [evidencias](entrega/evidencias/) contienen la salida de pytest, las pruebas
HTTP reales, OpenAPI y los datos del entorno y del artefacto.
