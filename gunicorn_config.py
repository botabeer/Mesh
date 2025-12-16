import os
import multiprocessing
from datetime import datetime

# -----------------------------
# اتصال وبيئة
# -----------------------------
PORT = int(os.getenv("PORT", 5000))
ENV = os.getenv("ENV", "production")  # "development" أو "production"

bind = f"0.0.0.0:{PORT}"
backlog = 2048

# -----------------------------
# عدد العمال والخيوط
# -----------------------------
cpu_count = multiprocessing.cpu_count()
if ENV == "development":
    workers = 1
    threads = 2
else:
    workers = min(cpu_count * 2 + 1, 6)  # الحد الأقصى 6 workers
    threads = 4

worker_class = "gthread"
worker_connections = 1000

# -----------------------------
# Requests
# -----------------------------
max_requests = 1000
max_requests_jitter = 50

timeout = 30               # زيادة timeout لـ webhook الطويلة
graceful_timeout = 20
keepalive = 5

# -----------------------------
# Logging
# -----------------------------
loglevel = "info"
accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s %(M)sms'

# إضافة طابع زمني لكل سجل
def post_fork(server, worker):
    worker.log.info(f"Worker spawned (pid: {worker.pid}) at {datetime.utcnow().isoformat()}")

# -----------------------------
# أداء وتحميل مسبق
# -----------------------------
preload_app = True
reload = ENV == "development"
worker_tmp_dir = "/dev/shm"

proc_name = "bot-mesh"
daemon = False
