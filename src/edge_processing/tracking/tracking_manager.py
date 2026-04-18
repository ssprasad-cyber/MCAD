from .track_packet import TrackPacket

class TrackingManager:

    def __init__(self, tracker):
        self.tracker = tracker


    def process(self, detection_packet):

        tracks = self.tracker.update(
            detection_packet.detections,
            detection_packet.frame
        )

        return TrackPacket(
            tracks=tracks,
            camera_id=detection_packet.camera_id,
            timestamp=detection_packet.timestamp,
            frame=detection_packet.frame
        )