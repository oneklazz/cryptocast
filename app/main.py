from fastapi import FastAPI
from pydantic import BaseModel
from core.forecast import make_forecast

app = FastAPI()

class ForecastRequest(BaseModel):
    coin: str
    days: int

@app.post("/predict")
async def predict(request: ForecastRequest):
    csv_path = f"dataset/coin_{request.coin}.csv"
    result = make_forecast(csv_path, request.days)
    return {
        "coin": request.coin,
        "days": request.days,
        "forecast": result
    }
