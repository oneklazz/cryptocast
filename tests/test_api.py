import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ── smoke tests ──────────────────────────────────────────────────────────────

def test_predict_endpoint_returns_200():
    """POST /predict returns 200 for valid coin and days"""
    response = client.post("/predict", json={"coin": "XRP", "days": 30})
    assert response.status_code == 200


def test_predict_endpoint_returns_correct_fields():
    """response contains coin, days and forecast fields"""
    response = client.post("/predict", json={"coin": "XRP", "days": 30})
    data = response.json()
    assert "coin" in data
    assert "days" in data
    assert "forecast" in data


def test_predict_endpoint_coin_matches_request():
    """coin in response matches the requested coin"""
    response = client.post("/predict", json={"coin": "XRP", "days": 5})
    assert response.json()["coin"] == "XRP"


# ── negative tests ────────────────────────────────────────────────────────────

def test_predict_endpoint_returns_422_for_missing_fields():
    """returns 422 when request body is missing required fields"""
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_endpoint_returns_error_for_unknown_coin():
    """returns error status for a coin with no dataset file"""
    response = client.post("/predict", json={"coin": "FAKECOIN", "days": 5})
    # Ожидаем любой код ошибки, но не 200
    assert response.status_code != 200
    # Или конкретно 404, если хотите строго:
    # assert response.status_code == 404
    assert "not found" in response.text.lower()


def test_predict_endpoint_returns_error_for_zero_days():
    """returns error when days is zero"""
    response = client.post("/predict", json={"coin": "XRP", "days": 0})
    assert response.status_code in (400, 422, 404, 500)
