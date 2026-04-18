"""
MCAD — Multi-Camera Anomaly Detection
Entry point. Edit camera_configs below to add/remove cameras.
Set MODEL_PATH env variable or pass --model to load trained weights.
"""

import os
import sys
import argparse
import threading
import cv2

from camera_layer.camera_factory import create_camera
from camera_layer.camera_manager import CameraManager

from edge_processing.frame_capture.frame_dispatcher import FrameDispatcher
from edge_processing.frame_capture.fps_controller import FPSController

from edge_processing.detection.yolov8_detector import YOLOv8Detector
from edge_processing.detection.detection_manager import DetectionManager

from edge_processing.tracking.deepsort_tracker import DeepSortTracker
from edge_processing.tracking.tracking_manager import TrackingManager

from edge_processing.pose_estimation.mediapipe_pose import MediaPipePose
from edge_processing.pose_estimation.pose_manager import PoseManager

from edge_processing.gnn.msgat_manager import MSGATManager

from utils.camera_worker import camera_worker
from utils.processing_worker import processing_worker
from utils.display_worker import display_worker


# -------------------------------------------------
# CLI
# -------------------------------------------------
parser = argparse.ArgumentParser(description="MCAD Real-Time Inference")
parser.add_argument("--model", type=str, default=os.environ.get("MODEL_PATH", ""),
                    help="Path to trained msgat_best.pt (optional)")
args, _ = parser.parse_known_args()


# -------------------------------------------------
# Camera Configuration
# Supported types: "file", "webcam", "rtsp", "mobile"
# -------------------------------------------------
camera_configs = [
    {"id": "cam1", "type": "file", "path": "data/raw/sample.mp4"},
    # {"id": "cam2", "type": "webcam", "index": 0},
]


# -------------------------------------------------
# Initialize Cameras
# -------------------------------------------------
cameras = [create_camera(cfg) for cfg in camera_configs]
manager = CameraManager(cameras)

# -------------------------------------------------
# Frame Dispatcher (buffer + rate control)
# -------------------------------------------------
dispatcher = FrameDispatcher(
    camera_ids=[cfg["id"] for cfg in camera_configs],
    buffer_size=20
)

fps = FPSController(target_fps=10)

# -------------------------------------------------
# Detection
# -------------------------------------------------
detector = YOLOv8Detector("yolov8n.pt")
detect_mgr = DetectionManager(detector)

# -------------------------------------------------
# Tracking
# -------------------------------------------------
tracker = DeepSortTracker()
tracking_mgr = TrackingManager(tracker)

# -------------------------------------------------
# Pose Estimation
# -------------------------------------------------
pose_model = MediaPipePose()
pose_mgr = PoseManager(pose_model)

# -------------------------------------------------
# GNN Inference (load weights if available)
# -------------------------------------------------
model_path = args.model or None
msgat_mgr = MSGATManager(model_path=model_path)

if model_path:
    print(f"Loaded MS-GAT weights from: {model_path}")
else:
    print("No trained model found — running with random weights (for demo only)")


print("MCAD Pipeline Started")
print("Press 'q' to quit\n")


try:
    t1 = threading.Thread(target=camera_worker, args=(manager,), daemon=True)
    t2 = threading.Thread(
        target=processing_worker,
        args=(detect_mgr, tracking_mgr, pose_mgr, msgat_mgr),
        daemon=True
    )
    t3 = threading.Thread(target=display_worker, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

except KeyboardInterrupt:
    print("\nStopping pipeline...")

finally:
    manager.release_all()
    cv2.destroyAllWindows()
    print("MCAD stopped cleanly")