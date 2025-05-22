# ============== Stage 1: Build dependencies ====================
FROM python:3.12-slim AS builder 

# Install OS-level dependencies (build-essential, etc.)
# RUN apt-get update && apt-get install -y --no-install-recommends \
# build-essential gcc libffi-dev libpq-dev curl && \
# rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install pip-tools to freeze dependencies
RUN pip install --upgrade pip setuptools wheel

# Install application dependencies
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# ============== Stage 2: Runtime ====================
FROM python:3.12-slim

LABEL maintainer="jeremy.rico35@gmail.com"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy installed packages from builder
COPY --from=builder /install /usr/local
COPY . /app

# Set working directory
WORKDIR /app

# Expose port
EXPOSE 8000

# Set non-root user for security
RUN adduser --disabled-password --no-create-home appuser && chown -R appuser /app
USER appuser

# Use Gunicorn + Uvicorn worker for production async performance
CMD ["gunicorn", "src.main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--workers", "1", "--threads", "2", "--timeout", "30"]
