# S10.7 — Informe de carga

## Cómo he medido

| Dato | Valor |
| --- | --- |
| API | `uv run --locked --group load fastapi dev --port 8100 --no-reload` (un proceso local) |
| Locust | `uv run --locked --group load locust -f locustfile.py --headless -u 20 -r 5 -t 1m --host http://127.0.0.1:8100 --csv reports/s10` |
| Carga | 20 usuarios con una rampa de 5 usuarios/s durante una prueba de 1 minuto |
| Cliente | `front`, con 60 peticiones por ventana de 60 s |
| Entorno | macOS 27.2.1, Apple Silicon (arm64), Locust 2.46.7, terminal de VS Code |

Configuré las claves de prueba en el `.env` local e inyecté la de `front` en
`LOCUST_API_KEY` al iniciar Locust. El peso de las tareas es 8 para predicción
válida, 1 para cuerpo inválido y 1 para salud.

[Estadísticas](s10_stats.csv) · [Fallos](s10_failures.csv) · [Histórico](s10_stats_history.csv) · [Excepciones](s10_exceptions.csv).

## Resultados

| Petición | Peticiones | RPS | p50 (ms) | p95 (ms) | Fallos | % 429 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `POST /v1/predictions` | 722 | 12,22 | 3 | 5 | 669 | 92,66 % |
| `POST /v1/predictions [422]` | 111 | 1,88 | 3 | 5 | 104 | 93,69 % |
| `GET /health` | 91 | 1,54 | 3 | 4 | 0 | — |
| Aggregated | 924 | 15,64 | 3 | 5 | 773 | 83,66 % |

El porcentaje divide los `429` registrados en `s10_failures.csv` por todas las
peticiones de la fila. Locust marca `422` como éxito en la tarea de cuerpo inválido.
Clasifica `429` como fallo en las dos tareas de predicción.

## Análisis

- Locust intentó 833 predicciones. Pasaron la cuota 53 válidas que acabaron en `200` y 7 inválidas que acabaron en `422`.
- Las 773 restantes recibieron `429`. Los dos tipos de petición cuentan porque la comprobación de cuota va antes de validar los campos del cuerpo.
- Salud tuvo p50 de 3 ms y p95 de 4 ms. Predicción con cuerpo válido tuvo p50 de 3 ms y p95 de 5 ms.
- Los percentiles de predicción incluyen respuestas `429`. Esta medida caracteriza la política de cuota bajo carga local.
- Con dos workers, cada proceso mantendría su propia ventana. Según cómo se repartiera el tráfico, un cliente podría consumir hasta dos cuotas.
- Para medir capacidad usaría un cliente de carga con cuota superior al tráfico previsto y mediría latencia de las peticiones exitosas por separado.
