from utils.pipeline_queue import frame_queue, result_queue
from edge_processing.graph.graph_manager import GraphManager
from edge_processing.graph.motion_memory import MotionMemory
from queue import Empty, Full


ALERT_CLASSES = {"fall", "fight", "fighting"}


def processing_worker(
        detect_mgr,
        tracking_mgr,
        pose_mgr,
        msgat_mgr):

    graph_mgr = GraphManager()
    motion_memory = MotionMemory()

    while True:
        try:
            pkt = frame_queue.get(timeout=0.05)
        except Empty:
            continue

        while True:
            try:
                pkt = frame_queue.get_nowait()
            except Empty:
                break

        det_pkt = detect_mgr.process(pkt)

        detected_alerts = sorted(
            {
                str(d.get("class_name", "")).strip().lower()
                for d in det_pkt.detections
                if str(d.get("class_name", "")).strip().lower() in ALERT_CLASSES
            }
        )

        det_pkt.detections = [
            d for d in det_pkt.detections
            if str(d.get("class_name", "")).strip().lower() == "person" and d["confidence"] > 0.5
        ]

        track_pkt = tracking_mgr.process(det_pkt)
        pose_mgr.process(track_pkt, pkt.frame)

        people = []
        for track in track_pkt.tracks:

            x1, y1, x2, y2 = map(int, track["bbox"])
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            gid = track["track_id"]
            vx, vy = motion_memory.compute(gid, (cx, cy))

            people.append({
                "gid": gid,
                "center": (cx, cy),
                "velocity": (vx, vy),
                "bbox_size": (x2 - x1) * (y2 - y1)
            })

        graph = graph_mgr.process(people)

        anomaly_score = msgat_mgr.predict(graph, people)

        output = (pkt.camera_id, pkt.frame, anomaly_score, detected_alerts)
        try:
            result_queue.put_nowait(output)
        except Full:
            try:
                result_queue.get_nowait()
            except Empty:
                pass

            try:
                result_queue.put_nowait(output)
            except Full:
                pass