# استخدام Python 3.11 slim كقاعدة
FROM python:3.11-slim

# إعداد متغيرات البيئة
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=10000 \
    DATABASE_URL=sqlite:///data/botmesh.db

WORKDIR /app

# تثبيت الأدوات الأساسية فقط
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# نسخ وتثبيت المتطلبات
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# نسخ جميع الملفات
COPY . .

# إنشاء مجلد البيانات وضبط الصلاحيات
RUN mkdir -p /app/data && chmod -R 755 /app/data

# أمر التشغيل باستخدام Gunicorn
CMD ["gunicorn", "app:app",
     "--bind", "0.0.0.0:${PORT}",
     "--workers", "1",
     "--threads", "4",
     "--worker-class", "gthread",
     "--timeout", "30",
     "--graceful-timeout", "15",
     "--keep-alive", "5",
     "--log-level", "info",
     "--access-logfile", "-",
     "--error-logfile", "-"]
