# cryptocast-core

Библиотека для прогнозирования цен криптовалют на основе модели Prophet

Является переиспользуемым ядром проекта [cryptocast](https://github.com/oneklazz/cryptocast)  
Может использоваться независимо от FastAPI-приложения - например, в CLI-утилитах, Telegram-ботах или пакетной обработке данных

## Возможности

- Прогнозирование цен закрытия на основе исторических данных (CSV)
- Поддержка монет: XRP, Ethereum, Dogecoin, Litecoin, Solana
- Возвращает список дат и соответствующих прогнозируемых цен

## Установка

### Из TestPyPI (рекомендуемый способ)

```bash
pip install -i https://test.pypi.org/simple/ cryptocast-core
```

### Локально

```bash
git clone https://github.com/onek1azz/cryptocast.git
cd cryptocast/core
pip install -e .
```

## Использование

```python
from core.forecast import make_forecast

# Прогноз на 30 дней на основе CSV-файла
result = make_forecast("dataset/coin_XRP.csv", days=30)

print(result["dates"])   # ['2024-01-01', '2024-01-02', ...]
print(result["values"])  # [0.52, 0.53, ...]
```

## Формат входных данных

### CSV-файл должен содержать колонки:

- Date - дата в формате YYYY-MM-DD
- Close - цена закрытия

## Возвращаемое значение
```python
{
    "dates": List[str],   # даты прогноза
    "values": List[float] # прогнозируемые значения
}
```
## Ошибки

| Исключение         | Условие |
|--------------------|----------|
| ValueError         | days <= 0 |
| FileNotFoundError	 | CSV-файл не найден |


## Требования

- Python >= 3.10
- pandas, prophet
