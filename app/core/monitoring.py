# app/core/monitoring.py
from flask import request
from prometheus_client import Counter, Histogram
import time
from functools import wraps

# Metrics
request_count = Counter(
    'flask_request_count', 
    'App Request Count',
    ['method', 'endpoint', 'http_status']
)

request_latency = Histogram(
    'flask_request_latency_seconds',
    'Request latency',
    ['endpoint']
)

def monitor_requests():
    """Monitoring middleware."""
    def middleware(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            response = f(*args, **kwargs)
            
            # Record request latency
            request_latency.labels(
                endpoint=request.endpoint
            ).observe(time.time() - start_time)
            
            # Record request count
            request_count.labels(
                method=request.method,
                endpoint=request.endpoint,
                http_status=response.status_code
            ).inc()
            
            return response
        return decorated_function
    return middleware