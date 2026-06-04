# cryptocast-core

Многоразовая библиотека для прогнозирования цен криптовалют с использованием Prophet

## Установка

```bash
pip install cryptocast-core
```

## Использование

```python
from forecast import make_forecast

result = make_forecast("path/to/coin.csv", days=30)
print(result["dates"])
print(result["values"])
```