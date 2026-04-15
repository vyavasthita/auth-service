# Auth Service

- A **production-ready JWT authentication and RBAC service**
- Issues RS256 tokens, exposes JWKS for zero-trust verification, and ships with full observability out of the box.

### Why Auth Service?

- **RS256 + JWKS.** Tokens are signed with RSA keys and verified via a standard `/.well-known/jwks.json` endpoint — downstream services validate tokens locally using [Token Validator](https://github.com/vyavasthita/token-validator) without sharing secrets.
- **Built-in observability.** Uses [Instrumentation Hub](https://github.com/vyavasthita/instrumentation-hub) to push logs, traces, and metrics to [OAAS](https://github.com/vyavasthita/oaas) — no observability code in the business logic.
- **Clean architecture.** FastAPI dependency injection, generic repository pattern, Liquibase migrations, and configuration via Pydantic settings. Business logic is fully testable in isolation.
- **Dev-ready in one click.** VS Code Dev Container boots MySQL, Liquibase, API, and phpMyAdmin automatically — no local tooling required.

```mermaid
flowchart LR
    Client --> FastAPI[Auth Service API]
    FastAPI --> MySQL[(MySQL)]
    FastAPI -.->|JWKS endpoint| JWKS[RS256 Public Keys]
    FastAPI -.->|instrumentation-hub| Collector[OAAS OTel Collector]
    Collector --> Grafana[Grafana / Loki / Tempo / Prometheus]
    Downstream[Downstream Services] -.->|JWKS + token-validator| JWKS
```

---

## Getting Started

### `.env` Configuration
- Configure [`.env`](.env) 

| Variable | Default | Description |
|----------|---------|-------------|
| `OBSERVABILITY_NETWORK_NAME` | `oaas-observability-net` | **Must match OAAS `.env`** |
| `SERVICE_NAME` | `auth-service` | Service name (OTEL resource + API root path) |
| `MYSQL_HOST_PORT` | `2001` | MySQL host port |
| `API_PORT` | `2002` | Auth Service API port |
| `PHPMYADMIN_HOST_PORT` | `2003` | phpMyAdmin port |
| `MYSQL_PORT` | `3306` | MySQL internal port (do not change) |

---

### Option A — Dev Container (Recommended)

**Prerequisites:** VS Code, Docker Desktop, [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

1. Clone this repo
2. Export secrets:
   ```bash
   export AUTH_SERVICE_MYSQL_ROOT_PASSWORD=yourpassword
   export AUTH_SERVICE_SECRET_KEY=yourjwtsecret
   ```
3. Open the folder in VS Code
4. When prompted, click **Reopen in Container**
5. All services (MySQL, Liquibase, API, phpMyAdmin) start automatically
6. Swagger UI: **http://localhost:<API_PORT>/auth-service/docs**

> Ensure [OAAS](https://github.com/vyavasthita/oaas) is running first for observability.

### Option B — Makefile

**Prerequisites:** Docker Desktop / Docker Engine + Compose, Make

1. Clone this repo
2. Run:
   ```bash
   export AUTH_SERVICE_MYSQL_ROOT_PASSWORD=yourpassword
   export AUTH_SERVICE_SECRET_KEY=yourjwtsecret
   make build   # first time or after dependency changes
   make up
   ```

Swagger UI: **http://localhost:<API_PORT>/auth-service/docs**

## Make Commands

| Command | Description |
|---------|-------------|
| `make build` | Build images (runs `poetry update` for instrumentation-hub) |
| `make up` | Start all services |
| `make stop` | Stop containers |
| `make down` | Stop + remove containers |
| `make clean` | Full cleanup (containers, volumes, caches) |
| `make test` | Run unit + functional tests |
| `make fmt` | Format code (ruff) |
| `make lint` | Lint code (ruff) |

---

## Service Endpoints

| Service | URL | Variable |
|---------|-----|----------|
| Auth API | http://localhost:<API_PORT>/auth-service/docs | `API_PORT` |
| MySQL | localhost:2001 | `MYSQL_HOST_PORT` |
| phpMyAdmin | http://localhost:<PHPMYADMIN_HOST_PORT> | `PHPMYADMIN_HOST_PORT` |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/register` | Register a new user |
| `POST` | `/login` | Authenticate and get JWT (RS256) |
| `POST` | `/session-status` | Check token session/revocation status |
| `GET` | `/token/.well-known/jwks.json` | JWKS public key endpoint |
| `GET` | `/health` | Database connectivity check |
| `POST` | `/roles` | Add a new role |
| `GET` | `/users/me` | Get current user details |

---

## Observability

Instrumented via [instrumentation-hub-fastapi](https://github.com/vyavasthita/instrumentation-hub) → pushes to [OAAS](https://github.com/vyavasthita/oaas):

- **Logs** → Loki / OpenSearch
- **Traces** → Tempo / Jaeger
- **Metrics** → Prometheus
- **Middleware** → request/response logging with sensitive field masking
- **Rate-limited logging** on `/health`

`OBSERVABILITY_NETWORK_NAME` must match across both repos for Docker DNS resolution.

---

## Related Repositories

| Repository | Purpose |
|------------|---------|
| [OAAS](https://github.com/vyavasthita/oaas) | Observability stack (Grafana, Loki, Tempo, Prometheus) |
| [Instrumentation Hub](https://github.com/vyavasthita/instrumentation-hub) | Client library for OpenTelemetry instrumentation |
| [Token Validator](https://github.com/vyavasthita/token-validator) | RS256 JWT validation library with JWKS support (used by consumer services) |

---

## License

Copyright © 2026 Dilip Kumar Sharma. All rights reserved.
