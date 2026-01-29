from collections import deque
import threading

class FrameBuffer:
    def __init__(self, max_size=30):
        self._buffer = deque(maxlen=max_size)
        self._lock = threading.Lock()

    def push(self, packet):
        with self._lock:
            self._buffer.append(packet)

    def pop(self):
        with self._lock:
            if not self._buffer:
                return None
            return self._buffer.popleft()

    def latest(self):
        with self._lock:
            if not self._buffer:
                return None
            return self._buffer[-1]

    def size(self):
        with self._lock:
            return len(self._buffer)
