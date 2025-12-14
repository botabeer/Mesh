import os
import multiprocessing

bind = f"0.0.0.0:{os.getenv('PORT', 5000)}"
backlog = 2048

workers = min(multiprocessing.cpu_count() * 2 + 1, 4)
worker_class = "sync"  # يمكن تغييره لـ "gthread" عند كثرة الwebhooks
threads = 2
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

timeout = 30
keepalive = 5
graceful_timeout = 30

accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

proc_name = "bot-mesh"

daemon = False
preload_app = True
reload = False
