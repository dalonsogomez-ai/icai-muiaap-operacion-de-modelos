"""Punto de entrada de la API: `fastapi dev` usa `wine_api.main:app`."""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from wine_api.errors import install_error_handlers
from wine_api.predictor import Predictor, build_predictor
from wine_api.request_id import request_id_middleware
from wine_api.routers import health, predictions

API_VERSION = "1.1.0"
OPENAPI_TAGS = [
    {"name": "health", "description": "Estado del servicio y del predictor."},
    {"name": "predictions", "description": "Predicción de la calidad de vino tinto."},
]


def create_app(predictor: Predictor | None = None) -> FastAPI:
    """Crea la aplicación; los tests inyectan su propio predictor."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        app.state.predictor = predictor or build_predictor(
            os.environ.get("WINE_API_MODE", "ready")
        )
        yield

    app = FastAPI(
        title="Wine Quality API",
        version=API_VERSION,
        summary="Predice la banda de calidad de vinos tintos.",
        description=(
            "Localiza cada petición con `request_id` o la cabecera `X-Request-Id`. "
            "Los errores comparten el sobre `ErrorResponse`. "
            "Usa `error.code` para decidir cómo tratarlos."
        ),
        openapi_tags=OPENAPI_TAGS,
        lifespan=lifespan,
    )
    app.middleware("http")(request_id_middleware)
    install_error_handlers(app)
    app.include_router(health.router)
    app.include_router(predictions.router)
    return app


app = create_app()
