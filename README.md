README: |
  # Auth Service

  ## About
 Authentication and authorization service for modern microservices.

  ---

  ## Key Features

  - JWT access
  - Token expiration
  - Role-Based Access Control (RBAC)
  - Service-to-service authentication
  - OpenTelemetry-based observability

  ---

  ## Tech Stack

  - **Backend Framework:** FastAPI (Python)
  - **Authentication:** JWT (access and refresh tokens)
  - **Authorization:** Role-Based Access Control (RBAC)
  - **Database:** MySql
  - **Observability:** OpenTelemetry
  - **Containerization:** Docker
  - **Orchestration:** Docker Compose

  ## Quick Start

  ```bash
  export AUTH_SERVICE_MYSQL_ROOT_PASSWORD=yourpassword
  make build   # first time or after dependency changes (e.g. instrumentation-hub update)
  make up
  ```

  Service available at: **http://localhost:5001/auth-service/docs**

  ---

  ## Run Tests

  ```bash
  cd components
  make app-test
  ```

  ---

  ## Architecture

  ```mermaid
  flowchart LR
      Client --> AuthController
      AuthController --> AuthService
      AuthService --> AuthRepository
      AuthRepository --> MySQL[(MySQL)]
  ```

  ### Request Lifecycle

  ```mermaid
  sequenceDiagram
      participant C as Client
      participant Ctrl as AuthController
      participant Svc as AuthServiceImpl
      participant Repo as AuthRepository
      participant DB as MySQL

      C->>Ctrl: POST /register
      Ctrl->>Svc: register(db_session, ...)
      Svc->>Repo: save(session, user)
      Repo->>DB: INSERT INTO users
      DB-->>Repo: user row
      Repo-->>Svc: User
      Svc-->>Ctrl: User
      Ctrl-->>C: 201 RegisterUserResponseDTO
  ```

  ---

  ## Core Roles

  | Layer | Class | Responsibility |
  |-------|-------|----------------|
  | Controller | `AuthController` | HTTP routing, request/response DTOs |
  | Service | `AuthServiceImpl` | Business logic, decorators (`is_new_user`, `is_valid_user`, `is_valid_token`) |
  | Repository | `AuthRepository` → `BaseRepository` | Async CRUD via `session.add` / `flush` |
  | Model | `User` | SQLAlchemy 2.0 `DeclarativeBase` + `Mapped` + `mapped_column()` |
  | Config | `Settings` | Composite pydantic-settings (MySQL, JWT, CORS, DB pool, observability) |

  ---

  ## Project Layout

  ```
  auth-service/
  ├── components/
  │   ├── Makefile                    # Aggregate make targets
  │   ├── docker-compose.yaml         # Root compose (includes app + db)
  │   ├── auth_service_app/
  │   │   ├── Dockerfile
  │   │   ├── Makefile
  │   │   ├── pyproject.toml
  │   │   ├── src/
  │   │   │   ├── api/
  │   │   │   │   ├── bootstrap/      # AppFactory, Initializer, CORS, Instrumentation
  │   │   │   │   ├── config/         # Split pydantic-settings (app, mysql, jwt, cors, ...)
  │   │   │   │   ├── constants/      # Frozen dataclass constants
  │   │   │   │   ├── controllers/    # AuthController, HealthController
  │   │   │   │   ├── dependencies/   # Config, DatabaseDependency
  │   │   │   │   ├── dtos/           # Request/Response DTOs
  │   │   │   │   ├── exceptions/     # Typed exceptions + handlers
  │   │   │   │   ├── models/         # SQLAlchemy 2.0 DeclarativeBase models
  │   │   │   │   ├── repos/          # Generic base repo + AuthRepository
  │   │   │   │   └── services/       # AuthService (abstract + impl)
  │   │   │   └── utils/              # Logger, Security, JWTUtils, email validator
  │   │   └── tests/
  │   └── auth_service_db/
  │       └── migrations/             # Liquibase changelogs
  └── README.md
  ```

  ---

  ## API Endpoints

  | Method | Path | Description |
  |--------|------|-------------|
  | `POST` | `/register` | Register a new user |
  | `POST` | `/login` | Authenticate and get JWT |
  | `POST` | `/validate-token` | Validate JWT and get user claims |
  | `GET` | `/app_health` | Application health check |
  | `GET` | `/db_health` | Database connectivity check |

  ---
## License

Copyright © 2026 Dilip Kumar Sharma

All rights reserved.

This repository is provided for reference and demonstration purposes only.  
No permission is granted to use, copy, modify, or distribute this code, in whole or in part, for any purpose without explicit written permission from the author.