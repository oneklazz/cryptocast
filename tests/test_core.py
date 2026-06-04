import pytest
import os
from core.forecast import make_forecast


# ── smoke tests ──────────────────────────────────────────────────────────────

def test_make_forecast_returns_dict(xrp_csv_path):
    """forecast returns a dict with dates and values keys"""
    result = make_forecast(xrp_csv_path, 30)
    assert isinstance(result, dict)
    assert "dates" in result
    assert "values" in result


def test_make_forecast_returns_correct_number_of_days(xrp_csv_path):
    """forecast returns exactly the requested number of future dates"""
    days = 7
    result = make_forecast(xrp_csv_path, days)
    assert len(result["dates"]) == days
    assert len(result["values"]) == days


def test_make_forecast_dates_are_strings(xrp_csv_path):
    """dates in forecast result are strings in YYYY-MM-DD format"""
    result = make_forecast(xrp_csv_path, 5)
    for date in result["dates"]:
        assert isinstance(date, str)
        assert len(date) == 10  # YYYY-MM-DD


def test_make_forecast_values_are_floats(xrp_csv_path):
    """predicted values are numeric"""
    result = make_forecast(xrp_csv_path, 5)
    for value in result["values"]:
        assert isinstance(value, (int, float))


# ── negative tests ────────────────────────────────────────────────────────────

def test_make_forecast_raises_for_missing_file():
    """raises exception when csv path does not exist"""
    with pytest.raises(Exception):
        make_forecast("dataset/coin_DOESNOTEXIST.csv", 30)


def test_make_forecast_raises_for_zero_days(xrp_csv_path):
    """raises ValueError when days is zero"""
    with pytest.raises(ValueError, match="days must be positive"):
        make_forecast(xrp_csv_path, 0)


def test_make_forecast_raises_for_negative_days(xrp_csv_path):
    """raises ValueError when days is negative"""
    with pytest.raises(ValueError, match="days must be positive"):
        make_forecast(xrp_csv_path, -5)
