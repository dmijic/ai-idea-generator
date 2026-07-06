install:
	pip install -r requirements.txt

run:
	uvicorn api:app --reload --host 127.0.0.1 --port 8000

test:
	python -m pytest tests

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

help:
	@echo "Dostupne komande:"
	@echo "  make install  - instaliraj dependencije"
	@echo "  make run      - pokreni API lokalno"
	@echo "  make test     - pokreni testove"
	@echo "  make build    - build i pokreni Docker"
	@echo "  make down     - ugasi Docker"

s:
	PYTHONPATH=. python random_scripts/scratch.py