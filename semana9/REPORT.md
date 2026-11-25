# Informe de la práctica 9 — Wine Quality API 1.1.0

## Leyenda utilizada

- `->` Objetivo o problema que quiero resolver.
- `~>` Decisión o cambio realizado y su justificación.
- `>` Acción técnica ejecutada.
- `>>` Evidencia verificable: archivo, salida o comprobación.
- `=>` Resultado obtenido y estado de verificación.

## Objetivo y trabajo realizado

`->` Convertí la API del starter en un servicio con contrato de salida, errores
consistentes y documentación reproducible. [Enunciado del workshop](modules/09-api-professional/exercises/02-wine-api-hardening/README.md).

`~>` Validé la salida a partir de los atributos del predictor. Serializo
`confidence` con hasta dos decimales y `served_at` en UTC con sufijo `Z`.
El contrato público contiene la banda, la confianza y las versiones del
modelo y del preprocesado. [FastAPI · modelos de respuesta](https://fastapi.tiangolo.com/tutorial/response-model/).

`~>` Separé JSON mal formado (`400`) de JSON que incumple el esquema
(`422`). Las rutas lanzan errores de dominio y un manejador central conserva
el sobre `ErrorResponse` y el `request_id`. Para un `500` devuelvo un mensaje
genérico y registro el identificador en el servidor.

`>` Probé un `503` con `dependency_overrides`, seis valores inválidos, los
extremos inclusivos del alcohol y la igualdad entre el OpenAPI generado y el
snapshot. Ejecuté pytest, Ruff y la exportación desde la terminal integrada de
VS Code. [Starter resuelto](modules/09-api-professional/exercises/02-wine-api-hardening/problem/starter/).

`>>` [Contrato OpenAPI](modules/09-api-professional/exercises/02-wine-api-hardening/problem/starter/contracts/openapi.json) ·
[Captura de Swagger](entrega/evidencias/swagger.jpg) ·
[Comprobaciones del workshop](entrega/evidencias/verificacion.txt).

## Clase 1 · Microejercicios

`>` Comparé las respuestas de las demos, probé el manejador de validación
por defecto de FastAPI y ejecuté el ejemplo `minor` desde Swagger. [Respuestas y evidencias](entrega/MICROEXERCISES.md).

## Compatibilidad

- Mantengo las rutas `POST /v1/predictions` y `GET /health` y la forma de sus entradas.
- Añado `served_at` a la salida. Un cliente que acepta campos nuevos puede ignorarlo.
- Si un cliente aplica un esquema cerrado, debe incorporar ese campo opcional a su lectura.
- Redondeo `confidence` en la respuesta y conservo su tipo numérico. El consumidor puede ver una diferencia de precisión.
- Quitar `request_id`, renombrar un campo obligatorio o cambiar el tipo de `confidence` rompería el contrato de S7.
- Publicaría esos cambios en una versión mayor con una ruta nueva y una guía de migración.

`=>` El workshop queda en la versión `1.1.0` con 33 tests en verde. Las demos
pasan 10 tests, incluido el caso de ingresos cero.
