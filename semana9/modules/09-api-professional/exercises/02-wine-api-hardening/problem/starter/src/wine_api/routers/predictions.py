from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Body

from wine_api.dependencies import PredictorDep, RequestIdDep
from wine_api.schemas import (
    VALID_FEATURES_EXAMPLE,
    ErrorResponse,
    Prediction,
    PredictionRequest,
    PredictionResponse,
)

EXAMPLES = {
    "valid": {
        "summary": "Vino dentro de los rangos",
        "value": {"features": VALID_FEATURES_EXAMPLE},
    },
    "wrong_type": {
        "summary": "Alcohol enviado como texto",
        "value": {"features": {**VALID_FEATURES_EXAMPLE, "alcohol": "mucho"}},
    },
    "out_of_range": {
        "summary": "pH fuera de rango",
        "value": {"features": {**VALID_FEATURES_EXAMPLE, "ph": 7.0}},
    },
}

router = APIRouter(
    prefix="/v1/predictions",
    tags=["predictions"],
    responses={
        400: {"model": ErrorResponse, "description": "JSON mal formado."},
        422: {"model": ErrorResponse, "description": "El cuerpo incumple el contrato."},
        503: {"model": ErrorResponse, "description": "Predictor no disponible."},
    },
)


@router.post(
    "",
    summary="Predecir la banda de calidad",
    response_description="Predicción, identificador de petición y fecha UTC.",
)
def create_prediction(
    payload: Annotated[PredictionRequest, Body(openapi_examples=EXAMPLES)],
    predictor: PredictorDep,
    request_id: RequestIdDep,
) -> PredictionResponse:
    """Predice con once variables numéricas y rangos inclusivos según WineFeatures.

    Devuelve la banda de calidad y la confianza redondeada a dos decimales.
    Usa el identificador de petición al informar de una incidencia.
    """

    output = predictor.predict(payload.features)
    # Leo solo los atributos del contrato público. `raw_score` queda dentro.
    return PredictionResponse(
        prediction=Prediction.model_validate(output, from_attributes=True),
        request_id=request_id,
        served_at=datetime.now(UTC),
    )
