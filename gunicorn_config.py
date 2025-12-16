import os
import multiprocessing

PORT = int(os.getenv("PORT", 8080))
ENV = os.getenv("ENV", "production")

bind = f"0.0.0.0:{PORT}"
backlog = 2048

cpu_count = multiprocessing.cpu_count()
if ENV == "development":
    workers = 1
    threads = 2
else:
    workers = min(cpu_count * 2 + 1, 8)
    threads = 4

worker_class = "gthread"
worker_connections = 1000

max_requests = 2000
max_requests_jitter = 100

timeout = 60
graceful_timeout = 30
keepalive = 5

loglevel = "info"
accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s %(M)sms'

preload_app = True
reload = ENV == "development"
worker_tmp_dir = "/dev/shm"

proc_name = "bot-mesh"
daemon = False
