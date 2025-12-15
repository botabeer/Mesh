import os
import multiprocessing

# Binding
bind = f"0.0.0.0:{os.getenv('PORT', 5000)}"
backlog = 2048

# Workers
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)
worker_class = "gthread"  # مهم للسرعة
threads = 4
worker_connections = 1000

# Requests
max_requests = 1000
max_requests_jitter = 50

# Timeouts - مهم جداً
timeout = 10  # تقليل من 30 إلى 10
keepalive = 2  # تقليل من 5 إلى 2
graceful_timeout = 15  # تقليل من 30 إلى 15

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s %(M)sms'

# Process
proc_name = "bot-mesh"
daemon = False
preload_app = True
reload = False

# Performance
worker_tmp_dir = "/dev/shm"  # استخدام RAM للملفات المؤقتة
