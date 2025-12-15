import os
import multiprocessing

bind = f"0.0.0.0:{os.getenv('PORT', 5000)}"
backlog = 2048

workers = min(multiprocessing.cpu_count() * 2 + 1, 4)
worker_class = "gthread"
threads = 4
worker_connections = 1000

max_requests = 1000
max_requests_jitter = 50

timeout = 10
keepalive = 2
graceful_timeout = 15

accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s %(M)sms'

proc_name = "bot-mesh"
daemon = False
preload_app = True
reload = False

worker_tmp_dir = "/dev/shm"
