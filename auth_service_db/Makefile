# Auth Service DB Makefile

DB_DIR:=$(abspath $(dir $(lastword $(MAKEFILE_LIST))))
DB_PROJECT_ROOT:=$(DB_DIR)
DB_DATA_DIR:=$(DB_PROJECT_ROOT)/data/database/mysql
DB_VOLUME=personal_assistant_auth-service-database_data
DB_STACK_FILE:=$(abspath $(DB_PROJECT_ROOT)/../docker-compose-auth-service.yaml)

.PHONY: db-clean db-build db-run db-stop

db-clean:
	rm -rf $(DB_DATA_DIR)
	mkdir -p $(DB_DATA_DIR)
	docker volume rm $(DB_VOLUME) || true
	@echo "Auth service database state cleaned."

db-build:
	docker compose -f $(DB_STACK_FILE) build auth-service-database auth-service-liquibase
	@echo "Auth service database images built."

db-run:
	docker compose -f $(DB_STACK_FILE) up -d auth-service-database auth-service-liquibase
	@echo "Auth service database stack running."

db-stop:
	docker compose -f $(DB_STACK_FILE) stop auth-service-liquibase auth-service-database
	@echo "Auth service database stack stopped."
