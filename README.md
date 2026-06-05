# cryptocast

Сервис прогнозирования цен криптовалют на основе модели Prophet.

FastAPI-приложение принимает название монеты и количество дней
и возвращает прогноз цены закрытия.

## Поддерживаемые монеты

XRP, Ethereum, Dogecoin, Litecoin, Solana

## Требования

- Python 3.10+
- Docker и Docker Compose

## Быстрый старт

```bash
make install
make run
```

Приложение доступно по адресу: http://localhost:8000/docs

### Запрос прогноза

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"coin": "XRP", "days": 30}'
```

## Команды

| Команда | Описание |
|---------|----------|
| `make help` | Показать все команды |
| `make install` | Установить зависимости |
| `make run` | Запустить приложение |
| `make test` | Запустить тесты |
| `make coverage` | Отчёт о покрытии |
| `make build-lib` | Собрать пакет core |
| `make publish-lib` | Опубликовать на TestPyPI |
| `make docs` | Собрать документацию |
| `make docker-up` | Запустить в Docker |
| `make check` | Полная проверка |
| `make clean` | Удалить артефакты |

## Структура проекта

```
.
├── app/            # FastAPI приложение
├── core/           # Переиспользуемая библиотека прогнозирования
├── dataset/        # CSV файлы с историческими ценами
├── docs/           # Документация (MkDocs)
├── tests/          # Тесты
├── Makefile        # Команды проекта
├── Dockerfile      # Образ приложения
└── docker-compose.yaml
```

## Пакет core

Библиотека `cryptocast-core` опубликована на TestPyPI:
https://test.pypi.org/project/cryptocast-core/0.1.0/

Установка:
```bash
pip install -i https://test.pypi.org/simple/ cryptocast-core
```
