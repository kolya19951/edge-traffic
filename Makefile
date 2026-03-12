install:
	python3 -m pip install -U pip
	pip install -e ".[dev]"

run-api:
	uvicorn apps.api.main:app --host 0.0.0.0 --port 8000

run-worker:
	python -m apps.worker.main

test:
	pytest

lint:
	ruff check .

check:
	make lint
	make test
