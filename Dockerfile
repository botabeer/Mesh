# استخدام Python 3.11
FROM python:3.11-slim

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ جميع الملفات
COPY . .

# تعريف المنفذ
ENV PORT=10000
EXPOSE 10000

# تشغيل البوت
CMD ["python", "app.py"]
