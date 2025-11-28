FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Use single worker to avoid database locks
CMD gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --timeout 120 --preload app:app
