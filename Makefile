.PHONY: install run test docker-up docker-down docs

install:
	python3 -m pip install -r requirements.txt

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
