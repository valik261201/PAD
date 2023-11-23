import time

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.state = "closed"
        self.last_failure_time = None

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"

    def reset(self):
        self.failures = 0
        self.state = "closed"

    def is_open(self):
        if self.state == "open" and (time.time() - self.last_failure_time) > self.reset_timeout:
            self.state = "half-open"
        return self.state == "open"

    def call(self, func, *args, **kwargs):
        if self.is_open():
            raise Exception("CircuitBreaker: Service is unavailable")

        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.reset()
            return result
        except Exception as e:
            self.record_failure()
            raise e
        
    def with_circuit_breaker(func):
    
    def wrapper(*args, **kwargs):
        if cb.is_open():
            return jsonify({'error': 'Service temporarily unavailable'}), 503
        try:
            return func(*args, **kwargs)
        except Exception as e:
            cb.record_failure()
            return jsonify({'error': f'Service error: {str(e)}'}), 500
    return wrapper