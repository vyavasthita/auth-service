# Auth Service DB Makefile

DB_DIR:=$(abspath $(dir $(lastword $(MAKEFILE_LIST))))
DB_PROJECT_ROOT:=$(DB_DIR)
DB_DATA_DIR:=$(DB_PROJECT_ROOT)/data/database/mysql
DB_VOLUME=auth-service-database-data
DB_STACK_FILE:=$(abspath $(DB_PROJECT_ROOT)/../../docker-compose.yaml)

.PHONY: db-stop db-down db-clean db-build db-up 

db-stop:
	docker compose -f $(DB_STACK_FILE) stop auth-service-liquibase auth-service-database auth-service-phpmyadmin
	@echo "Auth service database stack stopped."

.PHONY: db-down
db-down:
	@echo "[down] docker compose -f $(DB_STACK_FILE) down --remove-orphans"
	@docker compose -f $(DB_STACK_FILE) down --remove-orphans auth-service-liquibase auth-service-database auth-service-phpmyadmin

db-clean:
	rm -rf $(DB_DATA_DIR)
	mkdir -p $(DB_DATA_DIR)
	docker volume rm $(DB_VOLUME) || true
	@echo "Auth service database state cleaned."

db-build:
	docker compose -f $(DB_STACK_FILE) build auth-service-database auth-service-liquibase auth-service-phpmyadmin
	@echo "Auth service database images built."

db-up:
	docker compose -f $(DB_STACK_FILE) up -d auth-service-database auth-service-liquibase auth-service-phpmyadmin
	@echo "Auth service database stack running."


