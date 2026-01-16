import cv2
import time
from .base_camera import BaseCamera

class MobileCamera(BaseCamera):
    def __init__(self, camera_id, url):
        super().__init__(camera_id)
        self.cap = cv2.VideoCapture(url)

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        return {
            "camera_id": self.camera_id,
            "frame": frame,
            "timestamp": time.time()
        }

    def release(self):
        self.cap.release()
