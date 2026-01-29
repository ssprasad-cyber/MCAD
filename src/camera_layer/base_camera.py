from abc import ABC, abstractmethod

class BaseCamera(ABC):
    def __init__(self, camera_id: str):
        self.camera_id = camera_id

    @abstractmethod
    def read(self):
        """
        Returns:
            FramePacket dict OR None if frame not available
        """
        pass

    @abstractmethod
    def release(self):
        """Release camera resources"""
        pass
