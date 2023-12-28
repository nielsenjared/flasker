# Gunicorn config variables
# loglevel = "info"
# errorlog = "-"  # stderr
# accesslog = "-"  # stdout
# worker_tmp_dir = "/dev/shm"
# graceful_timeout = 120
# timeout = 120
# keepalive = 5
# threads = 3

from app import app

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=8000)