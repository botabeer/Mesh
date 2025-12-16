FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create volume for database
VOLUME ["/app/data"]

# Expose port
EXPOSE 8080

# Environment
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV PORT=8080
ENV DB_PATH=/app/data/botmesh.db

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Run
CMD ["gunicorn", "app:app", "-c", "gunicorn_config.py"]
