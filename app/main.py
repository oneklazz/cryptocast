from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.forecast import make_forecast
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "cryptocast API", "docs": "/docs"}

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

    Raises:
        HTTPException: 404 если файл с данными не найден
        HTTPException: 400 если days <= 0
    """
    csv_path = f"dataset/coin_{request.coin}.csv"
    
    # Проверяем существование файла перед вызовом forecast
    if not os.path.exists(csv_path):
        raise HTTPException(
            status_code=404,
            detail=f"Data for coin '{request.coin}' not found"
        )
    
    # Проверяем days > 0 (хотя это также проверяется в forecast, но лучше вернуть понятную ошибку)
    if request.days <= 0:
        raise HTTPException(
            status_code=400,
            detail="days must be positive"
        )
    
    try:
        result = make_forecast(csv_path, request.days)
        return {
            "coin": request.coin,
            "days": request.days,
            "forecast": result
        }
    except ValueError as e:
        # Дополнительная обработка других ValueError из forecast
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Любые другие ошибки — 500
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
