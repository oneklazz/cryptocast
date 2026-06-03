from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post("/predict", json={"coin": "XRP", "days": 30})
    assert response.status_code == 200
    data = response.json()
    assert "coin" in data
    assert "days" in data
    assert "forecast" in data
