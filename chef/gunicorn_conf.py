import os
workers = int(os.environ.get('GUNICORN_PROCESSES', '4'))
threads = int(os.environ.get('GUNICORN_THREADS', '2'))
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:1882')
forwarded_allow_ips = '*'
