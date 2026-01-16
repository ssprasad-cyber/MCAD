from collections import deque
import threading

class FrameBuffer:
    def __init__(self, max_size=30):
        self.buffer = deque(maxlen=max_size)
        self.lock = threading.Lock()

    def push(self, frame_packet):
        with self.lock:
            self.buffer.append(frame_packet)

    def pop(self):
        with self.lock:
            if len(self.buffer) == 0:
                return None
            return self.buffer.popleft()

    def latest(self):
        with self.lock:
            if len(self.buffer) == 0:
                return None
            return self.buffer[-1]

    def size(self):
        with self.lock:
            return len(self.buffer)
