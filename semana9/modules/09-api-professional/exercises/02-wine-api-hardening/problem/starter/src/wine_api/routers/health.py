from fastapi import APIRouter

from wine_api.dependencies import PredictorDep, RequestIdDep
from wine_api.errors import ModelUnavailableError
from wine_api.schemas import ErrorResponse, HealthResponse

SERVICE_NAME = "wine-quality-prediction"
router = APIRouter(
    tags=["health"],
    responses={
        503: {"model": ErrorResponse, "description": "Predictor no disponible."}
    },
)


@router.get(
    "/health",
    summary="Comprobar la disponibilidad",
    response_description="El servicio y el predictor están listos.",
)
def read_health(predictor: PredictorDep, request_id: RequestIdDep) -> HealthResponse:
    """Comprueba la disponibilidad antes de predecir.

    Un 503 indica que el predictor no está listo para servir inferencias.
    """

    if not predictor.is_ready():
        raise ModelUnavailableError()
    return HealthResponse(
        status="ok",
        service=SERVICE_NAME,
        model_status="ready",
        model_version=predictor.model_version,
        request_id=request_id,
    )
