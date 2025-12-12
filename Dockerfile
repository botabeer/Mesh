FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=10000

WORKDIR /app

# تثبيت المتطلبات الأساسية فقط
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# تثبيت باكجات بايثون
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# نسخ التطبيق
COPY . .

# مجلد آمن للبيانات
RUN mkdir -p /app/data \
    && chmod -R 755 /app/data

# الأوامر النهائية للتشغيل
CMD gunicorn \
    --bind 0.0.0.0:${PORT} \
    --workers 1 \
    --threads 4 \
    --worker-class gthread \
    --timeout 30 \
    --graceful-timeout 15 \
    --keep-alive 5 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    app:app
