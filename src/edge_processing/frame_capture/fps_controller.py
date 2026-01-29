import time

class FPSController:
    def __init__(self, target_fps):
        self.interval = 1.0 / target_fps
        self.last_tick = time.time()

    def sync(self):
        now = time.time()
        elapsed = now - self.last_tick

        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)

        self.last_tick = time.time()
