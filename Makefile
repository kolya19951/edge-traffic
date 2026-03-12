install:
	python3 -m pip install -U pip
	pip install -e ".[dev]"

run-api:
	uvicorn edge_traffic.api.main:app --host 0.0.0.0 --port 8000

run-worker:
	python -m edge_traffic.worker.main

test:
	pytest

lint:
	ruff check .

check:
	make lint
	make test
