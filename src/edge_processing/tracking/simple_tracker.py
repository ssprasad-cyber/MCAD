import numpy as np

def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)

    boxAArea = (boxA[2]-boxA[0])*(boxA[3]-boxA[1])
    boxBArea = (boxB[2]-boxB[0])*(boxB[3]-boxB[1])

    return interArea / float(boxAArea + boxBArea - interArea + 1e-6)


class SimpleTracker:

    def __init__(self):
        self.tracks = {}
        self.next_id = 1

    def update(self, detections):

        updated_tracks = []

        for det in detections:

            bbox = det["bbox"]

            best_id = None
            best_score = 0

            for track_id, track_bbox in self.tracks.items():

                score = iou(bbox, track_bbox)

                if score > best_score:
                    best_score = score
                    best_id = track_id

            if best_score > 0.3:
                self.tracks[best_id] = bbox
                track_id = best_id
            else:
                track_id = self.next_id
                self.tracks[track_id] = bbox
                self.next_id += 1

            updated_tracks.append({
                "track_id": track_id,
                "bbox": bbox,
                "confidence": det["confidence"],
                "class_name": det["class_name"]
            })

        return updated_tracks