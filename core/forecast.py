import pandas as pd
from prophet import Prophet


def make_forecast(csv_path: str, days: int) -> dict:
    """
    Выполняет прогноз цены криптовалюты на основе данных из csv-файла.

    Args:
        csv_path (str): путь к csv-файлу с колонками Date и Close
        days (int): количество дней для прогноза, должно быть > 0

    Returns:
        dict: словарь с ключами:
            - "dates" (list[str]): список будущих дат в формате YYYY-MM-DD
            - "values" (list[float]): список прогнозируемых цен

    Raises:
        ValueError: если days <= 0
        FileNotFoundError: если файл по csv_path не найден
    """
    if days <= 0:
        raise ValueError("days must be positive")

    df = pd.read_csv(csv_path)
    df = df[["Date", "Close"]]
    df.columns = ["ds", "y"]
    df["ds"] = pd.to_datetime(df["ds"])

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    last_date = df["ds"].max()
    future_forecast = forecast[forecast["ds"] > last_date]

    return {
        "dates": future_forecast["ds"].dt.strftime("%Y-%m-%d").tolist(),
        "values": future_forecast["yhat"].tolist(),
    }
