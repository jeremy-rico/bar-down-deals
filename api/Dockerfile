# Stage 1: base
FROM python:3.12-slim as base
ENV  POETRY_VERSION=2.0.1 \
	PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1 \
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100 \
	POETRY_HOME="/opt/poetry" \
	POETRY_VIRTUALENVS_IN_PROJECT=true \
	POETRY_NO_INTERACTION=1 \
	PYSETUP_PATH="/opt/pysetup" \
	VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Stage 2: builder
FROM base as builder
RUN --mount=type=cache,target=/root/.cache \
	pip install "poetry==$POETRY_VERSION"
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN --mount=type=cache,target=$POETRY_HOME/pypoetry/cache \
	poetry install --only main

# Stage 3: production
FROM base as production
ENV FASTAPI_ENV=production
COPY --from=builder $VENV_PATH $VENV_PATH
COPY . /app
WORKDIR /app
EXPOSE 8000
# One worker for ECS Fargate instance 0.25 vCPU 0.5 GB
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:8000"]
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
