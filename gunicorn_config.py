import os
import multiprocessing

ENV = os.getenv("ENV", "production")
PORT = int(os.getenv("PORT", 8080))

bind = f"0.0.0.0:{PORT}"

if ENV == "development":
    workers = 1
    threads = 2
    reload = True
else:
    cpu_count = multiprocessing.cpu_count()
    workers = min(cpu_count * 2 + 1, 8)
    threads = 4
    reload = False

worker_class = "gthread"

timeout = 30
graceful_timeout = 30
keepalive = 5

max_requests = 2000
max_requests_jitter = 100

loglevel = "info"
accesslog = "-"
errorlog = "-"

preload_app = True
proc_name = "bot-mesh"
daemon = False
