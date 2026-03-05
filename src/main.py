from camera_layer.camera_factory import create_camera
from camera_layer.camera_manager import CameraManager

from edge_processing.frame_capture.frame_packet import FramePacket
from edge_processing.frame_capture.frame_dispatcher import FrameDispatcher
from edge_processing.frame_capture.fps_controller import FPSController

from edge_processing.detection.yolov8_detector import YOLOv8Detector
from edge_processing.detection.detection_manager import DetectionManager

from edge_processing.tracking.deepsort_tracker import DeepSortTracker
from edge_processing.tracking.tracking_manager import TrackingManager

from edge_processing.pose_estimation.mediapipe_pose import MediaPipePose
from edge_processing.pose_estimation.pose_manager import PoseManager

from edge_processing.reid.appearance_encoder import AppearanceEncoder
from edge_processing.reid.global_identity_manager import GlobalIdentityManager

from edge_processing.graph.graph_manager import GraphManager
from edge_processing.graph.motion_memory import MotionMemory

from edge_processing.temporal.temporal_memory import TemporalMemory
from edge_processing.temporal.temporal_manager import TemporalManager

from edge_processing.gnn.msgat_manager import MSGATManager

import threading
import cv2

from utils.camera_worker import camera_worker
from utils.processing_worker import processing_worker
from utils.display_worker import display_worker


# -------------------------------------------------
# Camera Configuration
# -------------------------------------------------
camera_configs = [
    {"id": "cam1", "type": "file", "path": "data/raw/sample.mp4"},
    {"id": "cam2", "type": "webcam", "index": 0},
]


# -------------------------------------------------
# Initialize Cameras
# -------------------------------------------------
cameras = [create_camera(cfg) for cfg in camera_configs]
manager = CameraManager(cameras)


# -------------------------------------------------
# Frame Dispatcher
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
# Cross-camera ReID
# -------------------------------------------------
encoder = AppearanceEncoder()
global_id_mgr = GlobalIdentityManager()


# -------------------------------------------------
# Graph Construction
# -------------------------------------------------
graph_mgr = GraphManager()
motion_memory = MotionMemory()


# -------------------------------------------------
# Temporal Memory
# -------------------------------------------------
temporal_memory = TemporalMemory(window_size=10)
temporal_mgr = TemporalManager(temporal_memory)

# -------------------------------------------------
# GNN Model
# -------------------------------------------------
msgat_mgr = MSGATManager()



print("MCAD Pipeline Started")
print("Press 'q' to exit\n")


try:
    t1 = threading.Thread(target=camera_worker, args=(manager,))
    t2 = threading.Thread(target=processing_worker, args=(detect_mgr, tracking_mgr, pose_mgr, msgat_mgr))
    t3 = threading.Thread(target=display_worker)

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