# Bot Mesh - Dockerfile (Production Ready)
# Created by: Abeer Aldosari © 2025

FROM python:3.11-slim

# --- إعداد البيئة ---
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# --- تثبيت الأدوات الضرورية للبناء ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# --- نسخ وتثبيت المتطلبات ---
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# --- نسخ الكود ---
COPY . .

# --- إنشاء مجلد البيانات ---
RUN mkdir -p /app/data && chmod 755 /app/data

# --- فتح المنفذ ---
EXPOSE 5000

# --- أمر التشغيل الإنتاجي (Flask مثال) ---
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "3", "--threads", "2"]
