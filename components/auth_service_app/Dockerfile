FROM python:3.13.1-alpine3.21 AS requirements-stage

WORKDIR /tmp

# Install Poetry and git (git is required for VCS/git dependencies in pyproject.toml)
RUN apk add --no-cache git
RUN pip3 install poetry poetry-plugin-export

# Copy poetry files
COPY pyproject.toml /tmp
COPY poetry.lock /tmp

# Export poetry packages to requirements.txt, to be installed
RUN poetry export --without-hashes --with core -f requirements.txt --output requirements.txt

FROM python:3.13.1-alpine3.21

RUN apk update && apk add --no-cache \
    build-base \
    g++ \
    gcc \
    musl-dev \
    linux-headers \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    rust \
    curl \
    git

RUN pip3 install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements from previous stage to docker container in /app
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the src directory
COPY src /app/src

ARG API_PORT=5001
EXPOSE ${API_PORT}

CMD ["sh", "-c", "python -m uvicorn src.api:app --host 0.0.0.0 --port ${API_PORT}"]
