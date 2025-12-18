import os
import multiprocessing

ENV = os.getenv("ENV", "production")
PORT = int(os.getenv("PORT", 8080))

# الربط
bind = f"0.0.0.0:{PORT}"

# إعدادات Workers (مهم جداً لتجنب Timeout)
if ENV == "development":
    workers = 1
    threads = 2
    reload = True
else:
    # في الإنتاج: استخدام workers متعددة
    cpu_count = multiprocessing.cpu_count()
    workers = min(cpu_count * 2 + 1, 8)  # الحد الأقصى 8
    threads = 4  # كل worker لديه 4 threads
    reload = False

# نوع Worker (gthread مناسب للـ I/O المكثف)
worker_class = "gthread"

# Timeouts (مهم جداً)
timeout = 30          # Gunicorn timeout
graceful_timeout = 30 # وقت إيقاف سلس
keepalive = 5         # Keep-alive

# حدود الطلبات (لإعادة تشغيل Workers بشكل دوري)
max_requests = 2000
max_requests_jitter = 100

# السجلات
loglevel = "info"
accesslog = "-"
errorlog = "-"

# أداء
preload_app = True    # تحميل التطبيق قبل تفريع Workers
proc_name = "bot-mesh"
daemon = False
