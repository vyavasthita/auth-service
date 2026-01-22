# Auth Service Aggregate Makefile

include auth_service_db/Makefile

.PHONY: clean build test run stop

clean: db-clean app-clean
	rm -rf __pycache__
	@echo "Auth service cleaned."

build: db-build app-build
	@echo "Auth service images built."

test: app-test
	@echo "Auth service tested."

run: db-run app-run
	@echo "Auth service stack running."

stop: app-stop db-stop
	@echo "Auth service stack stopped."
