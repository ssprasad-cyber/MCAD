import cv2
from utils.pipeline_queue import result_queue
from queue import Empty


def display_worker():

    while True:
        try:
            cam_id, frame, anomaly = result_queue.get(timeout=0.05)
        except Empty:
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue

        while True:
            try:
                cam_id, frame, anomaly = result_queue.get_nowait()
            except Empty:
                break

        cv2.putText(
            frame,
            f"Anomaly {anomaly:.2f}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,255),
            2
        )

        cv2.imshow(cam_id, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break