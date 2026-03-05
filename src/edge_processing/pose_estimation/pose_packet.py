from dataclasses import dataclass
from typing import List, Dict

@dataclass
class PosePacket:
    camera_id: str
    timestamp: float
    poses: List[Dict]