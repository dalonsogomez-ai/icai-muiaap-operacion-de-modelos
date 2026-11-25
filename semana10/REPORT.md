# Informe de la práctica 10 — Wine Quality API 2.0.0

## Leyenda utilizada

- `->` Objetivo o problema que quiero resolver.
- `~>` Decisión o cambio realizado y su justificación.
- `>` Acción técnica ejecutada.
- `>>` Evidencia verificable: archivo, salida o comprobación.
- `=>` Resultado obtenido y estado de verificación.

## Objetivo y decisiones

`->` Protegí la API de predicción de S9 con identificación por cliente,
scopes, cuota y CORS configurables. [Enunciado de la práctica](modules/10-api-security/exercises/01-wine-api-security/README.md).

`~>` Cargué la configuración desde el entorno con `pydantic-settings`.
Usé `SecretStr` en la configuración y `secrets.compare_digest` para comparar la
clave al autenticar. Devuelvo el mismo `401` ante una clave ausente o inválida
y registro el `request_id` del intento. [FastAPI · APIKeyHeader](https://fastapi.tiangolo.com/reference/security/#fastapi.security.APIKeyHeader).

`~>` Declaré los permisos en el `APIRouter`. `front` puede predecir y `ops`
también puede consultar `/v1/admin/usage`. Aplico la cuota después del scope;
al agotarla, devuelvo `429` con `Retry-After` en segundos redondeados hacia
arriba. `/health` sigue disponible sin clave ni cuota.

`~>` Configuré orígenes CORS explícitos y expuse las cabeceras operativas
al navegador. Los preflight se resuelven en el middleware, antes de las
dependencias del router. [FastAPI · CORS](https://fastapi.tiangolo.com/tutorial/cors/).

## Ejecución

`>` Ejecuté pytest, Ruff, la exportación de OpenAPI y la carga desde la
terminal integrada de VS Code. Para Locust arranqué la API en localhost con
un proceso y mantuve los secretos locales en `.env`.

`>>` [Starter resuelto](modules/10-api-security/exercises/01-wine-api-security/problem/starter/) ·
[Contrato OpenAPI](modules/10-api-security/exercises/01-wine-api-security/problem/starter/contracts/openapi.json) ·
[Captura de Swagger](entrega/evidencias/swagger.jpg) ·
[Comprobaciones](entrega/evidencias/verificacion.txt) ·
[Informe y CSV de Locust](modules/10-api-security/exercises/01-wine-api-security/problem/starter/reports/README.md).

## Versionado y migración del front

- Paso a `2.0.0` porque exigir una clave cambia el contrato para los clientes anónimos.
- Mantengo el cuerpo de predicción y el sobre de error de S9.
- El gateway HTTP del front de S7 debe enviar `X-API-Key` al hacer `POST /v1/predictions`.
- Guardaría esa clave en los secretos de Streamlit o en una variable de entorno del servidor del front.
- El front puede distinguir `401` por credencial inválida, `403` por falta de permiso y `429` por cuota agotada.
- Para `429` usaría `Retry-After` para indicar cuánto queda hasta el siguiente intento.

`=>` Pasaron 78 tests, incluidos los 34 de regresión. En los CSV finales,
Locust registró 924 peticiones, 15,64 RPS agregadas y 5 ms de p95 agregado.
