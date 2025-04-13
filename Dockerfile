# NOTE: This dockerfile exclusivley runs the scraper app. However, since it was
# dependencies in /api (namely, the database models), it is placed the projects
# root directory as to give access to the whole project. 
# There is a Dockerfile and docker-compose.yml inside /api which runs the api
# daemon.

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
	# apt-get update \
	# && apt-get install -y libpq-dev gcc\
	pip install "poetry==$POETRY_VERSION"

WORKDIR $PYSETUP_PATH
COPY ./scraper/poetry.lock ./scraper/pyproject.toml ./
RUN --mount=type=cache,target=$POETRY_HOME/pypoetry/cache \
	poetry install --only main

# Stage 3: production
FROM base as production
# RUN apt-get update \
# && apt-get install -y libpq5 \
# && rm -rf /var/lib/apt/lists/*
# RUN apt-get update \ 
# 	&& apt-get install -y libpq-dev gcc\
# 	&& rm -rf /var/lib/apt/lists/*
COPY --from=builder $VENV_PATH $VENV_PATH
ENV PYTHONPATH="$PYTHONPATH:/app"
COPY ./api/src /app/api/src
COPY ./scraper /app/scraper
WORKDIR /app
CMD ["python3", "scraper/crawl.py"]
