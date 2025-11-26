# ============================================================================
# Bot Mesh v6.1 - Dockerfile
# صورة Docker احترافية ومحسنة
# ============================================================================

# استخدام Python 3.11 slim (خفيف وسريع)
FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات أولاً (للاستفادة من cache)
COPY requirements.txt .

# تثبيت المكتبات المطلوبة
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# إنشاء مستخدم غير root للأمان
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

# التبديل للمستخدم الجديد
USER botuser

# فتح المنفذ
EXPOSE 10000

# صحة الخادم
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:10000/health')" || exit 1

# تشغيل التطبيق باستخدام Gunicorn
CMD ["gunicorn", "app:app", \
     "--workers", "2", \
     "--threads", "4", \
     "--timeout", "120", \
     "--bind", "0.0.0.0:10000", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
