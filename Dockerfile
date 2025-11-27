# Bot Mesh v10.0 - Enhanced Dockerfile
# Created by: Abeer Aldosari © 2025

FROM python:3.11-slim

# تعيين المتغيرات البيئية
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# إنشاء user غير root للأمان
RUN useradd -m -u 1000 botmesh && \
    mkdir -p /app/data && \
    chown -R botmesh:botmesh /app

# تعيين مجلد العمل
WORKDIR /app

# نسخ requirements أولاً (للاستفادة من Docker cache)
COPY --chown=botmesh:botmesh requirements.txt .

# تثبيت المتطلبات
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    rm -rf ~/.cache/pip

# نسخ باقي الملفات
COPY --chown=botmesh:botmesh . .

# التبديل للـ user
USER botmesh

# المنفذ الافتراضي
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:10000/health', timeout=2)"

# أمر التشغيل
CMD ["gunicorn", "app:app", \
     "--bind", "0.0.0.0:${PORT:-10000}", \
     "--workers", "2", \
     "--threads", "4", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
