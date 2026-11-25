from fastapi import APIRouter, Depends

from wine_api.dependencies import RequestIdDep, SettingsDep
from wine_api.rate_limit import RateLimiterDep
from wine_api.schemas import ClientUsage, ErrorResponse, UsageResponse
from wine_api.security import require_scope

router = APIRouter(
    prefix="/v1/admin",
    tags=["admin"],
    dependencies=[Depends(require_scope("admin"))],
    responses={
        401: {"model": ErrorResponse, "description": "API key ausente o incorrecta."},
        403: {"model": ErrorResponse, "description": "Falta el scope admin."},
    },
)


@router.get(
    "/usage",
    summary="Consultar el consumo por cliente",
    response_description="Peticiones en la ventana activa y límite por cliente.",
)
def read_usage(
    settings: SettingsDep, limiter: RateLimiterDep, request_id: RequestIdDep
) -> UsageResponse:
    """Consulta el consumo de predicción durante la ventana actual de cada cliente."""

    # Expongo el contador y la cuota. La clave solo se lee al autenticar.
    return UsageResponse(
        clients=[
            ClientUsage(
                client=name,
                requests_in_window=limiter.usage(name),
                limit=config.rate_limit_per_minute,
            )
            for name, config in sorted(settings.clients.items())
        ],
        request_id=request_id,
    )
