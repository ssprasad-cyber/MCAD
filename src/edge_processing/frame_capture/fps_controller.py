import time

class FPSController:
    def __init__(self, target_fps):
        self.target_fps = target_fps
        self.frame_interval = 1.0 / target_fps
        self.last_time = time.time()

    def wait(self):
        now = time.time()
        elapsed = now - self.last_time

        if elapsed < self.frame_interval:
            time.sleep(self.frame_interval - elapsed)

        self.last_time = time.time()
