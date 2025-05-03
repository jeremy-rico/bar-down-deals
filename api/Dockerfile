# Use slim image to minimize size
FROM python:3.12-slim

# Set environment variables for security and performance
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=1 \
	PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	gcc \
	&& apt-get purge -y --auto-remove \
	&& rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . . 

# Expose FastAPI port (default)
EXPOSE 8000

# Use uvicorn with max performance settings for small ECS instance
# One worker for ECS Fargate instance 0.25 vCPU 0.5 GB
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:8000"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

