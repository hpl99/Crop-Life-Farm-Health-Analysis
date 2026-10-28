.PHONY: help up down ingest test lint

help:
	@echo "Nagpur Krishi Data Makefile"
	@echo "  make ingest  - Run the full real-data ingestion pipeline"
	@echo "  make test    - Run pytest test suite and CI guards"
	@echo "  make up      - Start Docker Compose services"
	@echo "  make down    - Stop Docker Compose services"

ingest:
	python packages/data-pipeline/src/ingestion/runner.py

test:
	pytest

up:
	docker compose -f infra/docker-compose.yml up -d

down:
	docker compose -f infra/docker-compose.yml down
