# Auth Service

<p align="left">
  <img src="https://img.shields.io/badge/python-3.13-blue" alt="Python 3.13" />
  <img src="https://img.shields.io/badge/framework-FastAPI-009688" alt="FastAPI" />
  <img src="https://img.shields.io/badge/auth-RS256%20%2B%20JWKS-orange" alt="RS256 + JWKS" />
  <img src="https://img.shields.io/badge/database-MySQL%208-4479A1" alt="MySQL" />
  <img src="https://img.shields.io/badge/observability-OpenTelemetry-blueviolet" alt="OpenTelemetry" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
</p>

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

## Skills Demonstrated

- **Asymmetric JWT signing (RS256 + JWKS)** — tokens are signed with a private RSA key; consuming services verify via a public JWKS endpoint, eliminating shared secrets across the platform.
- **Decorator-based authorization** — `@is_active_token` and `@is_new_user` decorators separate cross-cutting session/revocation checks from business logic, keeping service methods focused.
- **Generic repository pattern** — a single async base repository handles CRUD for all SQLAlchemy models; adding a new entity requires zero boilerplate.
- **Separation of concerns in token flow** — auth-service only validates sessions and revocation; JWT signature verification is delegated to consumer services via [token-validator](https://github.com/vyavasthita/token-validator), avoiding redundant self-validation.
- **Infrastructure-as-code observability** — logs, traces, and metrics are injected via [instrumentation-hub](https://github.com/vyavasthita/instrumentation-hub) with zero observability code in business logic; backend routing (Loki vs OpenSearch, Tempo vs Jaeger) is controlled entirely by environment variables.
- **Pydantic settings + environment-driven config** — all secrets, ports, and feature flags are loaded from environment variables with typed defaults, making the service 12-factor compliant.
- **Liquibase schema migrations** — database changes are versioned YAML changesets applied automatically on container startup, supporting safe rollbacks.
- **Comprehensive test strategy** — Automated tests across three layers: unit (isolated service/controller logic), functional (full FastAPI TestClient with mocked repos), and smoke tests (post-deploy HTTP validation against running containers).

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

## Testing

| Layer | Scope | Count |
|-------|-------|-------|
| Unit | Service logic, controllers, decorators, utilities | ~50 |
| Functional | Full request cycle via FastAPI TestClient with mocked repositories | ~30 |
| Smoke | Post-deploy HTTP tests against running Docker containers | ~7 |

Run all tests:
```bash
make test      # unit + functional
make smoke     # requires running containers
```

---

## License

[MIT](LICENSE) — Copyright © 2026 Dilip Kumar Sharma.
