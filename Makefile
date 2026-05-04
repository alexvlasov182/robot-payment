.PHONY: help install run test lint format type docker-build docker-run docker-test docker-quality clean

help:
	@echo "Robot Payment Platform Commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run application locally"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linter"
	@echo "  make format       - Format code"
	@echo "  make type         - Run type checking"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make docker-test  - Run tests in Docker"
	@echo "  make docker-quality - Run all quality checks in Docker"
	@echo "  make clean        - Clean cache files"

install:
	pip install -r requirements.txt
	pip install ruff mypy pytest pytest-cov httpx

# run:
# 	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# test:
# 	pytest -v --cov=app --cov-report=term-missing

# lint:
# 	ruff check app/

# format:
# 	ruff format app/

type:
	mypy app/ --ignore-missing-imports

build:
	docker build -t robot-payment-api .

run:
	docker-compose up -d

stop:
	docker-compose down

test:
	docker exec -it robot-api pytest -v --cov=app --cov-report=term-missing

lint:
	docker exec -it robot-api ruff check app/

format:
	docker exec -it robot-api ruff format app/

type:
	docker exec -it robot-api mypy app/ --ignore-missing-imports
