import time


class DistractionTracker:
    def __init__(self, config):
        self.threshold = config["threshold_seconds"]
        self.start_time = None

    def update(self, phone_detected):
        if phone_detected:
            if self.start_time is None:
                self.start_time = time.time()
            elif time.time() - self.start_time >= self.threshold:
                return True
        else:
            self.start_time = None

        return False
