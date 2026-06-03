import pytest
from core.forecast import make_forecast

def test_make_forecast_returns_dict():
    result = make_forecast("dataset/coin_XRP.csv", 30)
    assert isinstance(result, dict)
    assert "dates" in result
    assert "values" in result
