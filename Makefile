.PHONY: help up down ingest test build run-api run-web run

help:
	@echo "Nagpur Krishi Data Makefile"
	@echo "  make run      - Run both Backend and Frontend with a single command"
	@echo "  make ingest   - Run the full real-data ingestion pipeline"
	@echo "  make test     - Run pytest test suite and CI guards"
	@echo "  make build    - Build production Next.js frontend"
	@echo "  make run-api  - Run FastAPI backend on port 8000"
	@echo "  make run-web  - Run Next.js frontend on port 3000"
	@echo "  make up       - Start Docker Compose services"
	@echo "  make down     - Stop Docker Compose services"

run:
	python scripts/start_dev.py

ingest:
	python packages/data-pipeline/src/ingestion/runner.py

test:
	pytest

build:
	npm --prefix apps/web run build

run-api:
	uvicorn apps.api.src.main:app --host 127.0.0.1 --port 8000

run-web:
	npm --prefix apps/web run dev

up:
	docker compose -f infra/docker-compose.yml up -d

down:
	docker compose -f infra/docker-compose.yml down

