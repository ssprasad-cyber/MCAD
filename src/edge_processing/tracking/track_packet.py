from dataclasses import dataclass
from typing import List, Dict

@dataclass
class TrackPacket:
    camera_id: str
    timestamp: float
    tracks: List[Dict]