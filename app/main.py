from fastapi import FastAPI
from pydantic import BaseModel
from core.forecast import make_forecast

app = FastAPI()

class ForecastRequest(BaseModel):
    """
    модель запроса для эндпоинта /predict.
    """
    coin: str
    days: int

@app.post("/predict")
async def predict(request: ForecastRequest):

    """
    возвращает прогноз цены для указанной криптовалюты

    Args:
        request (ForecastRequest): тело запроса с полями coin и days

    Returns:
        dict: прогноз с полями coin, days, forecast
    """
    csv_path = f"dataset/coin_{request.coin}.csv"
    result = make_forecast(csv_path, request.days)
    return {
        "coin": request.coin,
        "days": request.days,
        "forecast": result
    }
