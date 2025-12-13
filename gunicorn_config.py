import os

# Server socket - استخدام PORT من البيئة
bind = f"0.0.0.0:{os.getenv('PORT', 10000)}"
backlog = 2048

# Worker processes - مهم جداً: gthread للمعالجة المتزامنة
workers = 2
worker_class = "gthread"
threads = 4
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeouts
timeout = 60
keepalive = 5
graceful_timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "bot-mesh"

# Server mechanics
daemon = False
preload_app = False

# Debugging
reload = False
