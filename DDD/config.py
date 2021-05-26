import os

def get_redis_host_and_port():
    host = os.environ.get("REDIS_HOST", "localhost")
    port = 63791 if host == "0.0.0.0" else 6379
    return dict(host=host, port=port)