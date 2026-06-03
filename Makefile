.PHONY: install run test docker-up docker-down docs

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

docs:
	mkdocs build