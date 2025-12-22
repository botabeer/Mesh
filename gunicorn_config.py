import os
import multiprocessing

# =================== الاعدادات الاساسية ===================
bind = f"0.0.0.0:{os.getenv('PORT', '8080')}"
workers = int(os.getenv("WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# =================== العمليات ===================
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# =================== التسجيل ===================
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# =================== الامان ===================
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# =================== الاداء ===================
worker_tmp_dir = "/dev/shm"

# =================== دورة حياة التطبيق ===================
def on_starting(server):
    """عند بدء الخادم"""
    print("🚀 Bot Mesh Starting...")

def on_reload(server):
    """عند اعادة التحميل"""
    print("🔄 Bot Mesh Reloading...")

def when_ready(server):
    """عند جاهزية الخادم"""
    print("✅ Bot Mesh Ready!")

def on_exit(server):
    """عند اغلاق الخادم"""
    print("👋 Bot Mesh Shutting Down...")

def worker_int(worker):
    """عند مقاطعة Worker"""
    print(f"⚠️ Worker {worker.pid} interrupted")

def worker_abort(worker):
    """عند فشل Worker"""
    print(f"❌ Worker {worker.pid} aborted")
