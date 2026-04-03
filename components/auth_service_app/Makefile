# Auth Service App Makefile

APP_DIR:=$(abspath $(dir $(lastword $(MAKEFILE_LIST))))
APP_PROJECT_ROOT:=$(APP_DIR)
APP_PARENT:=$(abspath $(APP_PROJECT_ROOT)/..)
APP_SRC_ROOT=src
APP_TEST_ROOT=tests
APP_TEST_REPORTS_IN_PROJECT=reports
APP_TEST_REPORTS_HOST=$(APP_PROJECT_ROOT)/reports
APP_VENV=$(APP_PROJECT_ROOT)/.venv
APP_VENV_BIN=$(APP_VENV)/bin
APP_STACK_FILE:=$(abspath $(APP_PROJECT_ROOT)/../../docker-compose.yaml)

export PYTHONPATH := $(APP_PROJECT_ROOT):$(APP_PARENT)

.PHONY: app-clean app-build app-up app-stop app-test app-pytest app-coverage

.PHONY: app-down
app-down:
	@echo "[down] docker compose -f $(APP_STACK_FILE) down --remove-orphans"
	@docker compose -f $(APP_STACK_FILE) down --remove-orphans auth-service smoke-tests

app-stop:
	docker compose -f $(APP_STACK_FILE) stop auth-service 
	@echo "Auth service app stack stopped."

app-clean:
	find $(APP_PROJECT_ROOT) -type d -name '__pycache__' -exec rm -rf {} +
	find $(APP_PROJECT_ROOT) -type d -name '.pytest_cache' -exec rm -rf {} +
	find $(APP_PROJECT_ROOT) -type f -name '*.pyc' -delete
	rm -rf $(APP_VENV)
	rm -rf $(APP_PROJECT_ROOT)/smoke_tests/.venv
	rm -rf $(APP_PROJECT_ROOT)/smoke_tests/output
	rm -rf $(APP_TEST_REPORTS_HOST)
	rm -f $(APP_PROJECT_ROOT)/.coverage
	@echo "Auth service app artifacts cleaned."

.PHONY: app-deps
app-deps:
	@echo "[app-deps] poetry update instrumentation-hub-fastapi before locking"
	@cd $(APP_DIR) && poetry update instrumentation-hub-fastapi
	@cd $(APP_DIR) && poetry lock

app-build: app-deps
	docker compose -f $(APP_STACK_FILE) build --no-cache auth-service smoke-tests

app-up:
	docker compose -f $(APP_STACK_FILE) up -d auth-service
	@echo "Auth service app running. Starting smoke tests..."
	docker compose -f $(APP_STACK_FILE) up smoke-tests

$(APP_VENV_BIN)/pytest:
	poetry install --no-root -C $(APP_PROJECT_ROOT)
	touch $@

app-pytest: $(APP_VENV_BIN)/pytest

$(APP_VENV_BIN)/coverage:
	poetry install --no-root -C $(APP_PROJECT_ROOT)
	touch $@

app-coverage: $(APP_VENV_BIN)/coverage

app-test: app-pytest app-coverage
	mkdir -p $(APP_TEST_REPORTS_HOST)
	PYTHONPATH=.:.. poetry run -C $(APP_PROJECT_ROOT) coverage run --source=$(APP_SRC_ROOT) -m pytest --log-cli-level=INFO --junit-xml $(APP_TEST_REPORTS_IN_PROJECT)/unit_tests.xml $(APP_TEST_ROOT)
	PYTHONPATH=.:.. poetry run -C $(APP_PROJECT_ROOT) coverage report -m
	PYTHONPATH=.:.. poetry run -C $(APP_PROJECT_ROOT) coverage xml -o $(APP_TEST_REPORTS_IN_PROJECT)/coverage.xml
	PYTHONPATH=.:.. poetry run -C $(APP_PROJECT_ROOT) coverage html -d $(APP_TEST_REPORTS_IN_PROJECT)/html
	@echo "Auth service app tests completed."