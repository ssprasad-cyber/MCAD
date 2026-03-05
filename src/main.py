from camera_layer.camera_factory import create_camera
from camera_layer.camera_manager import CameraManager

from edge_processing.frame_capture.frame_packet import FramePacket
from edge_processing.frame_capture.frame_dispatcher import FrameDispatcher
from edge_processing.frame_capture.fps_controller import FPSController

from edge_processing.detection.yolov8_detector import YOLOv8Detector
from edge_processing.detection.detection_manager import DetectionManager

from edge_processing.tracking.simple_tracker import SimpleTracker
from edge_processing.tracking.tracking_manager import TrackingManager

from edge_processing.pose_estimation.mediapipe_pose import MediaPipePose
from edge_processing.pose_estimation.pose_manager import PoseManager

import cv2


# -------------------------------------------------
# Camera Configuration
# -------------------------------------------------
camera_configs = [
    {"id": "cam1", "type": "file", "path": "data/raw/sample.mp4"},
    {"id": "cam2", "type": "webcam", "index": 0},
    # {"id": "mobile_cam", "type": "mobile", "url": "http://10.27.196.235:8080/video"},
]


# -------------------------------------------------
# Initialize Cameras
# -------------------------------------------------
cameras = [create_camera(cfg) for cfg in camera_configs]
manager = CameraManager(cameras)


# -------------------------------------------------
# Frame Dispatcher (Stage 2)
# -------------------------------------------------
dispatcher = FrameDispatcher(
    camera_ids=[cfg["id"] for cfg in camera_configs],
    buffer_size=20
)


# -------------------------------------------------
# FPS Controller
# -------------------------------------------------
fps = FPSController(target_fps=10)


# -------------------------------------------------
# Detection (Stage 3)
# -------------------------------------------------
detector = YOLOv8Detector("yolov8n.pt")
detect_mgr = DetectionManager(detector)


# -------------------------------------------------
# Tracking (Stage 4)
# -------------------------------------------------
tracker = SimpleTracker()
tracking_mgr = TrackingManager(tracker)


# -------------------------------------------------
# Pose Estimation (Stage 5)
# -------------------------------------------------
pose_model = MediaPipePose()
pose_mgr = PoseManager(pose_model)


print("MCAD Pipeline Started")
print("Press 'q' to exit\n")


try:

    while True:

        # -----------------------------------------
        # Read frames from cameras
        # -----------------------------------------
        packets = manager.read_all()

        for pkt in packets:

            frame_packet = FramePacket(
                camera_id=pkt["camera_id"],
                frame=pkt["frame"],
                timestamp=pkt["timestamp"]
            )

            dispatcher.push(frame_packet)


        # -----------------------------------------
        # Get synchronized frames
        # -----------------------------------------
        synced_frames = dispatcher.pull_latest()


        for cam_id, pkt in synced_frames.items():

            frame = pkt.frame


            # -----------------------------
            # Detection
            # -----------------------------
            det_pkt = detect_mgr.process(pkt)


            # -----------------------------
            # Filter only people
            # -----------------------------
            det_pkt.detections = [
                d for d in det_pkt.detections
                if d["class_name"] == "person" and d["confidence"] > 0.5
            ]


            # -----------------------------
            # Tracking
            # -----------------------------
            track_pkt = tracking_mgr.process(det_pkt)


            # -----------------------------
            # Pose Estimation
            # -----------------------------
            pose_pkt = pose_mgr.process(track_pkt, frame)


            # -----------------------------
            # Draw Tracks
            # -----------------------------
            for track in track_pkt.tracks:

                x1, y1, x2, y2 = map(int, track["bbox"])
                track_id = track["track_id"]

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID {track_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )


            # -----------------------------
            # Draw Pose Keypoints
            # -----------------------------
            for pose in pose_pkt.poses:

                for x, y in pose["keypoints"]:

                    px = int(x * frame.shape[1])
                    py = int(y * frame.shape[0])

                    cv2.circle(frame, (px, py), 3, (0, 0, 255), -1)


            # -----------------------------
            # Display frame
            # -----------------------------
            cv2.imshow(cam_id, frame)


        # -----------------------------------------
        # FPS Control
        # -----------------------------------------
        fps.sync()


        # -----------------------------------------
        # Exit Key
        # -----------------------------------------
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


except KeyboardInterrupt:
    print("\nStopping pipeline...")


finally:

    manager.release_all()
    cv2.destroyAllWindows()

    print("MCAD stopped cleanly")