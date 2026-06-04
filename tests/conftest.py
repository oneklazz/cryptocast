import pytest
import os
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def xrp_csv_path():
    """Путь к датасету XRP относительно корня проекта."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, "dataset", "coin_XRP.csv")
