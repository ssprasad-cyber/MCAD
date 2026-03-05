from dataclasses import dataclass
from typing import List

@dataclass
class DetectionPacket:

    def __init__(self, camera_id, frame, detections, timestamp):

        self.camera_id = camera_id
        self.frame = frame
        self.detections = detections
        self.timestamp = timestamp