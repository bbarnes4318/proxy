"""Gunicorn configuration for production deployment"""
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
backlog = 2048

# Worker processes - MINIMAL for memory constraints
workers = int(os.environ.get('GUNICORN_WORKERS', '1'))  # Use environment variable
worker_class = 'sync'
worker_connections = 1000
timeout = 30  # Increased timeout
keepalive = 2
max_requests = 1000  # Restart workers after 1000 requests
max_requests_jitter = 50  # Add some randomness

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'proxy-access-portal'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed later)
# keyfile = None
# certfile = None

