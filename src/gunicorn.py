import os

from src.settings import APP_HOST, APP_PORT

bind = f"{APP_HOST}:{APP_PORT}"
workers = 1 if os.environ.get("ENVIRONMENT") != "prd" else 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = int(workers * worker_connections)
keepalive = 2
max_requests_jitter = 5
timeout = 30
