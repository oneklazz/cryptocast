PYTHON = python3
PIP = pip3

.PHONY: help install run test coverage build-lib publish-lib install-lib-local docs docker-up docker-down check clean

help:
	@printf '%s\n' \
	  'install              Install all dependencies' \
	  'run                  Run the FastAPI application' \
	  'test                 Run all tests' \
	  'coverage             Run tests and show coverage report' \
	  'build-lib            Build the core package (dist/)' \
	  'publish-lib          Publish core package to TestPyPI' \
	  'install-lib-local    Install locally built core package' \
	  'docs                 Build MkDocs documentation' \
	  'docker-up            Build and start containers' \
	  'docker-down          Stop and remove containers' \
	  'check                Run tests + build-lib + docs' \
	  'clean                Remove generated artefacts'

install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e ./packages

run:
	uvicorn app.main:app --reload

test:
	pytest tests/ -v

coverage:
	pytest tests/ --cov=core --cov=app --cov-report=term-missing

build-lib:
	cd packages && $(PYTHON) -m build

publish-lib:
	twine upload --repository testpypi packages/dist/*

install-lib-local:
	$(PIP) install packages/dist/*.whl --force-reinstall

docs:
	mkdocs build

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

check: test build-lib docs

clean:
	rm -rf packages/dist packages/build site .coverage coverage/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
