#!/usr/bin/env python

import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 1000
worker_class = 'gevent'
worker_connections = 1000
graceful_timeout = 30
keepalive = 5
debug = True
daemon = True
accesslog = "/applogs/gunicorn_access.log"
errorlog = "/applogs/gunicorn_error.log"
