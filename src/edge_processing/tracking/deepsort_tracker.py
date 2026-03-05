from deep_sort_realtime.deepsort_tracker import DeepSort


class DeepSortTracker:

    def __init__(self):

        self.tracker = DeepSort(
            max_age=30,
            n_init=3,
            nms_max_overlap=1.0,
            max_cosine_distance=0.3
        )


    def update(self, detections, frame):

        dets = []

        for d in detections:

            x1, y1, x2, y2 = d["bbox"]

            w = x2 - x1
            h = y2 - y1

            dets.append([
                [x1, y1, w, h],
                d["confidence"],
                d["class_name"]
            ])


        tracks = self.tracker.update_tracks(dets, frame=frame)

        results = []

        for t in tracks:

            if not t.is_confirmed():
                continue

            track_id = t.track_id
            l, t_, r, b = map(int, t.to_ltrb())

            results.append({
                "track_id": track_id,
                "bbox": [l, t_, r, b]
            })

        return results