import cv2
from utils.pipeline_queue import result_queue
from queue import Empty
import time


SIREN_ALERTS = {"fall", "fight", "fighting"}
SIREN_COOLDOWN_SECONDS = 2.0


def _ring_siren():
    print("\a", end="", flush=True)


def display_worker():
    last_siren_at = 0.0

    while True:
        try:
            payload = result_queue.get(timeout=0.05)
        except Empty:
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue

        if len(payload) == 4:
            cam_id, frame, anomaly, detected_alerts = payload
        else:
            cam_id, frame, anomaly = payload
            detected_alerts = []

        while True:
            try:
                payload = result_queue.get_nowait()
            except Empty:
                break

            if len(payload) == 4:
                cam_id, frame, anomaly, detected_alerts = payload
            else:
                cam_id, frame, anomaly = payload
                detected_alerts = []

        # Colour-coded anomaly score bar
        bar_color = (0, 200, 0) if anomaly < 0.4 else (0, 140, 255) if anomaly < 0.7 else (0, 0, 255)
        h, w = frame.shape[:2]
        bar_w = int(anomaly * min(w // 3, 200))
        cv2.rectangle(frame, (20, 20), (20 + min(w // 3, 200), 44), (50, 50, 50), -1)
        cv2.rectangle(frame, (20, 20), (20 + bar_w, 44), bar_color, -1)
        cv2.putText(
            frame,
            f"Anomaly: {anomaly:.2f}",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            bar_color,
            2
        )

        active_siren_alerts = sorted(
            {
                str(alert).strip().lower()
                for alert in detected_alerts
                if str(alert).strip().lower() in SIREN_ALERTS
            }
        )

        if active_siren_alerts:
            cv2.putText(
                frame,
                f"ALERT: {', '.join(active_siren_alerts).upper()}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            now = time.time()
            if now - last_siren_at >= SIREN_COOLDOWN_SECONDS:
                _ring_siren()
                last_siren_at = now

        cv2.imshow(cam_id, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break