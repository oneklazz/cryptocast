import json
import os

import redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from core.forecast import make_forecast

app = FastAPI()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

class ForecastRequest(BaseModel):
    coin: str
    days: int

@app.post("/predict")
async def predict(request: ForecastRequest):
    csv_path = f"dataset/coin_{request.coin}.csv"

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail=f"Data for coin '{request.coin}' not found")

    if request.days <= 0:
        raise HTTPException(status_code=400, detail="days must be positive")

    cache_key = f"{request.coin}:{request.days}"

    try:
        cached = redis_client.get(cache_key)
        if cached:
            return {"coin": request.coin, "days": request.days, "forecast": json.loads(cached), "cached": True}
    except redis.RedisError:
        pass

    try:
        result = make_forecast(csv_path, request.days)
        try:
            redis_client.setex(cache_key, 3600, json.dumps(result))
        except redis.RedisError:
            pass
        return {"coin": request.coin, "days": request.days, "forecast": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
