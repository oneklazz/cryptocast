# Cryptocast

**Микросервис для прогноза криптовалют**

## Описание

**Проект позволяет пользователю выбрать криптовалюту (XRP, BTC, ETH и др.) и 
получить прогноз ее цены на заданное количество дней.
Прогноз строится с использованием модели Prophet.**

## Установка

### Через TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ cryptocast
```

## Use-case диаграмма

```mermaid
flowchart LR
    User(User) -->|Request forecast| API(API)
    API -->|Return forecast| User
```
## Sequence диаграмма

```mermaid
sequenceDiagram
    User->>API: POST /predict
    API->>Redis: check cache
    alt cache hit
        Redis-->>API: return cached
    else cache miss
        API->>Core: compute forecast
        Core-->>API: result
        API->>Redis: store result
    end
    API-->>User: JSON forecast
```
