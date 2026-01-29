from dataclasses import dataclass
import numpy as np

@dataclass
class FramePacket:
    camera_id: str
    frame: np.ndarray
    timestamp: float
