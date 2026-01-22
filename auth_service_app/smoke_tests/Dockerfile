FROM python:3.13.1-alpine3.21 AS requirements-stage

WORKDIR /tmp

# Install Poetry
RUN pip3 install poetry poetry-plugin-export

# Copy poetry files
COPY pyproject.toml /tmp
COPY poetry.lock /tmp

# Export poetry packages to requirements.txt, to be installed
RUN poetry export --without-hashes -f requirements.txt --output requirements.txt

FROM python:3.13.1-alpine3.21

RUN pip3 install --upgrade pip

# # set environment variables
# # Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=1

# # Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements from previous stage to docker container in /app 
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# # Copy everything from ./api directory to /app in the container
COPY tests/ /app/tests
COPY run.sh /app

ENTRYPOINT [ "sh", "run.sh"]
