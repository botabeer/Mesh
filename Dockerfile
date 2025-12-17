FROM python:3.11-slim

# ==================================================
# Workdir
# ==================================================

WORKDIR /app


# ==================================================
# Dependencies
# ==================================================

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ==================================================
# Application
# ==================================================

COPY . .


# ==================================================
# Persistent Data
# ==================================================

VOLUME ["/app/data"]


# ==================================================
# Environment
# ==================================================

ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV PORT=8080
ENV DB_PATH=/app/data/botmesh.db


# ==================================================
# Health Check
# ==================================================

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:' + __import__('os').environ.get('PORT', '8080') + '/health')"


# ==================================================
# Run (Gunicorn)
# ==================================================

CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
