
# Production-ready Dockerfile for Mesh-main
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1

# system deps for common packages (pillow, numpy, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Use the cleaned requirements file if present
RUN pip install --upgrade pip setuptools wheel
RUN if [ -f requirements-cleaned.txt ]; then pip install -r requirements-cleaned.txt; elif [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Create unprivileged user and switch
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

ENV FLASK_ENV=production
EXPOSE 8080

# Use gunicorn for production. The app exposes 'app' in app.py
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "--workers", "2", "--timeout", "120"]
