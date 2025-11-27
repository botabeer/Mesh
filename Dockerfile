FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Use PORT environment variable (Render provides this)
CMD gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 2 --timeout 120 app:app
