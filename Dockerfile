FROM python:3.11-slim

# تعطيل إنشاء ملفات .pyc وتفعيل unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# نسخ متطلبات التثبيت أولاً (للاستفادة من Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي الملفات
COPY . .

# إنشاء مجلد البيانات
RUN mkdir -p /app/data

# المنفذ الافتراضي (يمكن تعديله بمتغير البيئة)
EXPOSE 5000

# أمر التشغيل مع دعم متغير PORT
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 120
