DOCKER_TEST = docker exec -it robot-api

.PHONY: docker-test docker-lint docker-format docker-type docker-quality

docker-test:
	$(DOCKER_TEST) pytest -v --cov=app --cov-report=term-missing

docker-lint:
	$(DOCKER_TEST) ruff check app/

docker-lint-fix:
	$(DOCKER_TEST) ruff check --fix app/

docker-format:
	$(DOCKER_TEST) ruff format app/

docker-type:
	$(DOCKER_TEST) mypy app/ --ignore-missing-imports

docker-quality: docker-lint docker-format docker-type docker-test
	@echo "✅ All quality checks passed"