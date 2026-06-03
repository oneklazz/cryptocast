import pandas as pd
from prophet import Prophet

def make_forecast(csv_path: str, days: int) -> dict:
    df = pd.read_csv(csv_path)
    df = df[['Date', 'Close']]
    df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['ds'])
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    return {
        "dates": forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
        "values": forecast['yhat'].tolist()
    }
