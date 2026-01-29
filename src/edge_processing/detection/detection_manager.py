from .detection_packet import DetectionPacket

class DetectionManager:
    def __init__(self, detector):
        self.detector = detector

    def process(self, frame_packet):
        detections = self.detector.detect(frame_packet.frame)

        return DetectionPacket(
            camera_id=frame_packet.camera_id,
            timestamp=frame_packet.timestamp,
            detections=detections
        )
