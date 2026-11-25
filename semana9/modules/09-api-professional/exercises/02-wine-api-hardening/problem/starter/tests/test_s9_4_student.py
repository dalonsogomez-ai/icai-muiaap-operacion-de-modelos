"""Comprobaciones del contrato desde el punto de vista del cliente."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from wine_api.dependencies import get_predictor
from wine_api.export_openapi import render_openapi
from wine_api.predictor import UnavailablePredictor


def test_prediction_returns_503_when_model_is_unavailable(
    client: TestClient,
    valid_payload: dict,
) -> None:
    # Sustituyo la dependencia durante esta prueba y después la restauro.
    overrides = client.app.dependency_overrides
    overrides[get_predictor] = UnavailablePredictor
    try:
        response = client.post("/v1/predictions", json=valid_payload)
    finally:
        del overrides[get_predictor]

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "model_unavailable"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("alcohol", 4.99),
        ("alcohol", 20.01),
        ("density", 0.9799),
        ("ph", None),
        ("residual_sugar", "1.9"),
        ("sulphates", True),
    ],
)
def test_out_of_contract_values_are_rejected(
    client: TestClient,
    valid_payload: dict,
    field: str,
    value: object,
) -> None:
    valid_payload["features"][field] = value

    response = client.post("/v1/predictions", json=valid_payload)

    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "validation_error"
    assert [item["field"] for item in error["fields"]] == [f"features.{field}"]


@pytest.mark.parametrize("alcohol", [5, 20])
def test_range_limits_are_inclusive(
    client: TestClient,
    valid_payload: dict,
    alcohol: float,
) -> None:
    valid_payload["features"]["alcohol"] = alcohol

    assert client.post("/v1/predictions", json=valid_payload).status_code == 200


def test_openapi_matches_versioned_contract() -> None:
    snapshot = Path(__file__).resolve().parents[1] / "contracts/openapi.json"
    assert json.loads(render_openapi()) == json.loads(
        snapshot.read_text(encoding="utf-8")
    )
