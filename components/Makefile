# Auth Service Aggregate Makefile

include auth_service_db/Makefile
include auth_service_app/Makefile

NAME := Auth Service API
REPO_URL := https://github.com/vyavasthita/auth-service
COMPOSE_FILE ?= docker-compose.yaml
OBSERVABILITY_NETWORK_NAME ?= oaas-observability-net
API_IMAGE := auth-service-api:latest
API_LOCAL_PORT ?= 5001
.DEFAULT_GOAL := help


.PHONY: help
help:
	@echo "Welcome to $(NAME)!"
	@echo "Repository: $(REPO_URL)"
	@echo "Use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  up           build images, ensure networks, and start containers"
	@echo "  down         remove containers and anonymous volumes"
	@echo "  stop         stop running containers"
	@echo "  clean        stop, remove, and prune Docker artifacts"
	@echo "  build        rebuild images without cache"
	@echo "  deps         regenerate backend/poetry.lock after toolkit changes"
	@echo "  ps           show container status"
	@echo "  logs         follow docker compose logs"
	@echo ""
	@echo "Choose one option!"

.PHONY: all
all: clean up

.PHONY: stop
stop:
	@echo "[stop] docker compose -f $(COMPOSE_FILE) stop"
	$(MAKE) -C auth_service_db db-stop
	$(MAKE) -C auth_service_app app-stop

.PHONY: down
down:
	@echo "[down] docker compose -f $(COMPOSE_FILE) down --remove-orphans"
	$(MAKE) -C auth_service_db db-down
	$(MAKE) -C auth_service_app app-down

.PHONY: clean
clean: down
	@echo "[clean] delegating service-specific cleanup"
	@$(MAKE) -C auth_service_db db-clean
	@$(MAKE) -C auth_service_app app-clean

	@echo "[clean] tearing down containers and anonymous volumes"
	@docker compose -f $(COMPOSE_FILE) down -v --remove-orphans || true

	@echo "[clean] removing all Docker volumes (including database)"
	@docker volume prune -f >/dev/null
	@docker volume rm $$(docker volume ls -q) 2>/dev/null || true

	@echo "[clean] pruning stopped containers"
	@docker container prune -f >/dev/null
	
	@echo "[clean] pruning unused images"
	@docker image prune -f >/dev/null || true

.PHONY: observability-network
observability-network:
	@if docker network inspect $(OBSERVABILITY_NETWORK_NAME) >/dev/null 2>&1; then \
		echo "[network] docker network $(OBSERVABILITY_NETWORK_NAME) found"; \
	else \
		echo "[network] not found"; \
		exit 1; \
	fi

.PHONY: build
build:
	@echo "[build] docker compose -f $(COMPOSE_FILE) build --no-cache"
	$(MAKE) -C auth_service_db db-build
	$(MAKE) -C auth_service_app app-build

.PHONY: up
up: stop observability-network
	@echo "[up] docker compose -f $(COMPOSE_FILE) up -d --build --remove-orphans"
	$(MAKE) -C auth_service_db db-up
	$(MAKE) -C auth_service_app app-up

.PHONY: ps
ps:
	@docker compose -f $(COMPOSE_FILE) ps -a

.PHONY: logs
logs:
	@docker compose -f $(COMPOSE_FILE) logs -f

# Root-level test target
.PHONY: test
test:
	$(MAKE) -C auth_service_app app-test
	@echo "Auth service tested."