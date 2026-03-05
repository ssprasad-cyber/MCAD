from .detection_packet import DetectionPacket

class DetectionManager:

    def __init__(self, detector):
        self.detector = detector

    def process(self, frame_packet):

        detections = self.detector.detect(frame_packet.frame)

        return DetectionPacket(
            frame_packet.camera_id,
            frame_packet.frame,
            detections,
            frame_packet.timestamp
        )