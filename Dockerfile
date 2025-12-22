FROM python:3.11-slim

# تثبيت dependencies للنظام
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# نسخ requirements أولاً (للاستفادة من cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# إنشاء مجلد البيانات
RUN mkdir -p data && chmod 755 data

# Environment Variables
ENV PORT=8080
ENV DB_PATH=/app/data/botmesh.db
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

# تشغيل مع إشارات الإغلاق الصحيحة
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
