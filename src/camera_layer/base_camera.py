from abc import ABC, abstractmethod

class BaseCamera(ABC):
    def __init__(self, camera_id: str):
        self.camera_id = camera_id

    @abstractmethod
    def read(self):
        """Return FramePacket or None"""
        pass

    @abstractmethod
    def release(self):
        pass
