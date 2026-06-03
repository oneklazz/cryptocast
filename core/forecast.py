import pandas as pd
from prophet import Prophet

def make_forecast(csv_path: str, days: int) -> dict:
    """
    выполняет прогноз цены криптовалюты на основе данных из csv-файла

    Args:
        csv_path (str): путь к csv-файлу с данными
        days (int): кол-во дней для прогноза

    Returns:
        dict: словарь с ключами "dates" (список дат) и "values" (список прогнозов)
    """
    df = pd.read_csv(csv_path)
    df = df[['Date', 'Close']]
    df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['ds'])
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    # фильтр, только будущие даты
    last_date = df['ds'].max()
    future_forecast = forecast[forecast['ds'] > last_date]
    return {
        "dates": forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
        "values": forecast['yhat'].tolist()
    }
