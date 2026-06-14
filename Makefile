SHELL := /bin/bash
.SHELLFLAGS := -eo pipefail -c

PYTHON      ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else command -v python3; fi)
COMPOSE     ?= docker compose
CONTAINER   ?= robot-api
PYTEST_ARGS ?=

.PHONY: help install install-dev run test test-cov lint lint-fix format typecheck check clean \
        docker-build docker-up docker-up-detached docker-down docker-reset docker-logs docker-shell docker-test

help:
	@echo ""
	@echo "Robot Payment Platform"
	@echo ""
	@echo "  Local (uses .venv if present)"
	@echo "  make install        Install runtime dependencies"
	@echo "  make install-dev    + ruff, mypy, pytest, httpx"
	@echo "  make run            Start API on :8000 with reload"
	@echo "  make test           Run tests"
	@echo "  make test-cov       Run tests with coverage"
	@echo "  make check          lint + typecheck + test (run before commit)"
	@echo "  make clean          Delete cache folders"
	@echo ""
	@echo "  Docker"
	@echo "  make docker-build          Build images"
	@echo "  make docker-up             Start stack, logs in terminal"
	@echo "  make docker-up-detached    Start stack in background"
	@echo "  make docker-down           Stop stack"
	@echo "  make docker-reset          Stop stack and delete volumes (clean DB)"
	@echo "  make docker-logs           Follow API logs"
	@echo "  make docker-shell          Shell inside API container"
	@echo "  make docker-test           Run pytest inside container"
	@echo ""
	@echo "  Tip: make test PYTEST_ARGS=\"-k auth\""
	@echo ""

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

install-dev: install
	$(PYTHON) -m pip install ruff mypy pytest pytest-cov httpx

run:
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(PYTHON) -m pytest app/tests $(PYTEST_ARGS)

test-cov:
	$(PYTHON) -m pytest --cov=app --cov-report=term-missing app/tests $(PYTEST_ARGS)

lint:
	$(PYTHON) -m ruff check app/

lint-fix:
	$(PYTHON) -m ruff check --fix app/
	$(PYTHON) -m ruff format app/

format:
	$(PYTHON) -m ruff format app/

typecheck:
	$(PYTHON) -m mypy app/ --ignore-missing-imports

check: lint typecheck test

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage
	find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true

docker-build:
	$(COMPOSE) build

docker-up:
	$(COMPOSE) up --build

docker-up-detached:
	$(COMPOSE) up -d --build

docker-down:
	$(COMPOSE) down

docker-reset:
	$(COMPOSE) down -v

docker-logs:
	$(COMPOSE) logs -f $(CONTAINER)

docker-shell:
	$(COMPOSE) exec $(CONTAINER) sh

docker-test:
	$(COMPOSE) exec -T $(CONTAINER) python -m pytest app/tests $(PYTEST_ARGS)