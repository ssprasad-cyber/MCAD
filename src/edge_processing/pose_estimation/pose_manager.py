from .pose_packet import PosePacket

class PoseManager:

    def __init__(self, pose_model):
        self.pose_model = pose_model

    def process(self, track_packet, frame):

        poses = []

        for track in track_packet.tracks:
            x1,y1,x2,y2 = map(int, track["bbox"])

            pad = 20

            x1 = max(0, x1 - pad)
            y1 = max(0, y1 - pad)
            x2 = min(frame.shape[1], x2 + pad)
            y2 = min(frame.shape[0], y2 + pad)

            person_crop = frame[y1:y2, x1:x2]

            if person_crop.size == 0:
                continue

            keypoints = self.pose_model.estimate(person_crop)

            poses.append({
                "track_id": track["track_id"],
                "keypoints": keypoints
            })

        return PosePacket(
            camera_id=track_packet.camera_id,
            timestamp=track_packet.timestamp,
            poses=poses
        )