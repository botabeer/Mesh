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
    workers = min(cpu_count * 2 + 1, 4)
    threads = 2
    reload = False

worker_class = "gthread"

timeout = 60
graceful_timeout = 30
keepalive = 5

max_requests = 1000
max_requests_jitter = 50

loglevel = "info"
accesslog = "-"
errorlog = "-"

preload_app = True
proc_name = "bot-mesh-web"
daemon = False

def post_fork(server, worker):
    server.log.info(f"Worker spawned (pid: {worker.pid})")

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info(f"Worker received INT or QUIT signal (pid: {worker.pid})")

def worker_abort(worker):
    worker.log.info(f"Worker received SIGABRT signal (pid: {worker.pid})")
