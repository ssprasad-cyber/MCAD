from dataclasses import dataclass
from typing import List, Dict
import numpy as np

@dataclass
class TrackPacket:
    camera_id: str
    timestamp: float
    frame: np.ndarray
    tracks: List[Dict]