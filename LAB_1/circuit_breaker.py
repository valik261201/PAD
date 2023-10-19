import time

class CircuitBreaker:
    def __init__(self, max_failures=3, reset_timeout=10):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.state = "CLOSED"
        self.last_failed = None

    def reset(self):
        self.failures = 0
        self.state = "CLOSED"

    def trip(self):
        self.state = "OPEN"
        self.last_failed = time.time()

    def call(self, fn, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failed > self.reset_timeout:
                self.state = "HALF-OPEN"
            else:
                print("Circuit is OPEN. Cannot make the call.")
                return None

        try:
            result = fn(*args, **kwargs)
            if self.state == "HALF-OPEN":
                self.reset()
            return result
        except Exception as e:
            self.failures += 1
            if self.failures >= self.max_failures:
                self.trip()
            raise e