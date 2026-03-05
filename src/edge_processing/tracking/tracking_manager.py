from .track_packet import TrackPacket

class TrackingManager:

    def __init__(self, tracker):
        self.tracker = tracker

    def process(self, detection_packet):

        tracks = self.tracker.update(detection_packet.detections)

        return TrackPacket(
            camera_id=detection_packet.camera_id,
            timestamp=detection_packet.timestamp,
            tracks=tracks
        )