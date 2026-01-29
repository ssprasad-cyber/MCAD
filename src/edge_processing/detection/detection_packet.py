from dataclasses import dataclass
from typing import List

@dataclass
class DetectionPacket:
    camera_id: str
    timestamp: float
    detections: List[dict]
