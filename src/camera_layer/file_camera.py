import cv2
import time
from .base_camera import BaseCamera

class FileCamera(BaseCamera):
    def __init__(self, camera_id, video_path):
        super().__init__(camera_id)
        self.cap = cv2.VideoCapture(video_path)

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
