README: |
  # Auth Service

  Production-ready authentication and authorization service for modern backend systems.

  This service provides OAuth2-compliant authentication, JWT-based authorization, role-based access control (RBAC), and secure service-to-service authentication. It is designed to be stateless, scalable, observable, and cloud-native.

  ---

  ## Key Features

  - OAuth2 authentication flows
  - JWT access and refresh tokens
  - Token rotation and expiration
  - Role-Based Access Control (RBAC)
  - Service-to-service authentication
  - API key support
  - OpenTelemetry-based observability
  - Prometheus metrics and structured logging
  - Horizontal scalability
  - Docker and Kubernetes ready

  ---

  ## Tech Stack

  - **Backend Framework:** FastAPI (Python)
  - **Authentication:** OAuth2, JWT (access and refresh tokens)
  - **Authorization:** Role-Based Access Control (RBAC)
  - **Database:** PostgreSQL (system of record)
  - **Cache / Ephemeral Storage:** Redis
  - **Observability:** OpenTelemetry
  - **Metrics:** Prometheus
  - **Tracing:** Tempo or Jaeger
  - **Logging:** Loki
  - **Containerization:** Docker
  - **Orchestration:** Docker Compose, Kubernetes
  - **Deployment:** Helm charts

  ---

  ## Architecture Overview

    ```mermaid
    flowchart TD
        Client[Client]
        Backend[Backend Services]
        Auth[Auth Service]
        DB[(PostgreSQL)]
        Cache[(Redis)]
        Prom[Prometheus]
        Graf[Grafana]
        Loki[Loki]
        Trace[Tempo / Jaeger]

        Client -->|Login / Refresh| Auth
        Backend -->|JWT / API Key| Auth
        Auth -->|Users, Roles| DB
        Auth -->|Tokens, Rate Limits| Cache
        Auth -->|Metrics| Prom
        Auth -->|Logs| Loki
        Auth -->|Traces| Trace
        Prom --> Graf
    ```

  ---

  ## Redis Usage

  Redis is used for short-lived and security-sensitive data that requires fast access and automatic expiration (TTL).

  Primary use cases:

  - Refresh token storage and rotation
  - Token revocation and blacklisting
  - Rate limiting for authentication endpoints
  - Temporary OAuth2 authorization state
  - Password reset and email verification tokens

  Redis is **not** used as a system of record. PostgreSQL remains the authoritative datastore.

  ---

  ## Authentication Flow – Login

    ```mermaid
    sequenceDiagram
        participant Client
        participant Auth
        participant DB
        participant Redis

        Client->>Auth: POST /login (credentials)
        Auth->>DB: Validate user credentials
        DB-->>Auth: User record
        Auth->>Redis: Store refresh token (TTL)
        Auth-->>Client: Access token + Refresh token
    ```

  ---

  ## Authentication Flow – Token Refresh

    ```mermaid
    sequenceDiagram
        participant Client
        participant Auth
        participant Redis

        Client->>Auth: POST /token/refresh
        Auth->>Redis: Validate refresh token
        Redis-->>Auth: Token valid
        Auth->>Redis: Rotate refresh token
        Auth-->>Client: New access token + New refresh token
    ```

  ---

  ## Authentication and Authorization

  Authentication supports OAuth2 flows including username/password and client credentials.

  Authorization is implemented using JWTs with embedded claims and role-based access control.

  Access tokens are short-lived. Refresh tokens are rotated on every use to reduce replay risk.

  Service-to-service authentication is supported using API keys or OAuth2 client credentials.

  ---

  ## Observability

  The service is instrumented using OpenTelemetry from the ground up.

  It exposes:

  - Distributed traces for request flows
  - Metrics such as request latency, error rates, and authentication failures
  - Structured logs correlated with traces

  The service integrates with Prometheus, Grafana, Loki, Tempo, and Jaeger.

  ---

  ## Threat Model and Security Considerations

  ### Threats Addressed

  - **Brute force login attacks** – mitigated using Redis-backed rate limiting
  - **Token replay attacks** – mitigated using short-lived access tokens and refresh token rotation
  - **Token theft** – mitigated using HTTPS, short token lifetimes, and revocation support
  - **Privilege escalation** – mitigated using RBAC and strict claim validation
  - **Stolen refresh tokens** – mitigated using one-time-use refresh tokens and rotation
  - **Unauthorized service access** – mitigated using service-to-service authentication and API keys

  ### Security Best Practices

  - Passwords are stored as salted hashes
  - Secrets are injected via environment variables
  - Tokens include issuer, audience, and expiration claims
  - No sensitive data is logged
  - Authentication endpoints are rate limited

  ---

  ## Getting Started

  ### Prerequisites

  - Docker
  - Docker Compose

  ### Running Locally

    Before running the service, export the MySQL root password environment variable:

    ```bash
    export AUTH_SERVICE_MYSQL_ROOT_PASSWORD=yourpassword
    docker-compose up --build
    ```


  Service will be available at:

  - http://localhost:5001/auth-service


---

## API Endpoints

- `POST /auth-service/login`
- `POST /auth-service/register`
- `GET /auth-service/app_health`
- `GET /auth-service/db_health`

---

## Testing

The project includes unit and integration tests.

  ```bash
  make test
  ```

---

## Deployment

- Production-ready Docker image
- Configuration via environment variables
- Designed for horizontal scaling and zero-downtime deployments

---

## Use Cases

- SaaS platforms
- Microservice architectures
- Internal developer platforms
- API-first products
- AI and data platforms

---

## Why This Project

This project demonstrates real-world backend engineering practices including secure authentication, scalable architecture, observability-first design, and clean code organization.

It is intended as a reference implementation of a production-grade authentication service.

---

## Author

Dilip Kumar Sharma 
Backend Engineer | Distributed Systems | Observability | Security

---

## License

Copyright © 2026 Dilip Kumar Sharma

All rights reserved.

This repository is provided for reference and demonstration purposes only.  
No permission is granted to use, copy, modify, or distribute this code, in whole or in part, for any purpose without explicit written permission from the author.
