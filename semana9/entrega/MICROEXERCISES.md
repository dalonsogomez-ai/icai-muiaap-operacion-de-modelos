# Microejercicios de la semana 9

## M1 · Serialización

`>` Comparé `/v1/scores/leaky`, `/v1/scores/public` y `/v1/scores/filtered`.
Solo la primera respuesta expone `raw_score` y `threshold_config`. En
`filtered`, `response_model=PublicScore` filtra los campos del diccionario
que no declara el modelo público. El esquema `PublicScore` muestra
`is_reliable`, el campo calculado del resultado.

## M2 · Errores

`>>` Estas fueron las respuestas de las peticiones indicadas. Añadí el caso de
modelo no disponible para comprobar también el quinto error.

| Petición | Status | `error.code` | `error.fields` |
| --- | ---: | --- | --- |
| `POST` con edad 30 e ingresos 1000 | 200 | — | — |
| `POST` con edad `"treinta"` | 422 | `validation_error` | `age` |
| `POST` sin ingresos | 422 | `validation_error` | `income` |
| `GET /v1/nada` | 404 | `not_found` | — |
| `GET /v1/boom` | 500 | `internal_error` | — |
| `POST` con el modelo no disponible | 503 | `model_unavailable` | — |

Los cinco fallos tenían `error` en la raíz y sus cuerpos omitían
`TU_SECRETO`. Sustituí temporalmente el manejador de validación por el de
FastAPI. El `422` volvió a presentar `detail` e incluyó `input: "treinta"`.
Restauré el manejador de la demo al terminar.

## M3 · OpenAPI

`>` En `paths["/v1/scores"]["post"]`, el título está en `summary`, el docstring
en `description` y los errores documentados en `responses`. Añadí `no_income`
junto a `valid` y `minor` en `requestBody.content["application/json"].examples`.

`>>` Ejecuté `minor` desde **Try it out** y obtuve `422` sobre `age`. Esta
demo de documentación devuelve el `detail` predeterminado de FastAPI.
Actualicé la comprobación de OpenAPI para exigir los tres ejemplos.
[Swagger de la demo](evidencias/swagger-microejercicio.jpg).

## M4 · Tests

`>` Encontré el override en `test_dependency_override_simulates_unavailable_model`.
Al usar el valor por defecto `raise_server_exceptions=True`, TestClient
propagó el `RuntimeError` de `/v1/boom` y no pude inspeccionar el sobre HTTP
desde el test. Volví a usar `False` y añadí un test que envía `income: 0` y
comprueba `422` y `error.fields[0].field == "income"`.

`=>` 10 tests en verde y Ruff en verde. [Salida de la ejecución](evidencias/microejercicios.txt).
