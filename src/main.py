from camera_layer.camera_factory import create_camera
from camera_layer.camera_manager import CameraManager
from edge_processing.frame_capture.frame_packet import FramePacket
from edge_processing.frame_capture.frame_dispatcher import FrameDispatcher
from edge_processing.frame_capture.fps_controller import FPSController
from edge_processing.detection.yolov8_detector import YOLOv8Detector
from edge_processing.detection.detection_manager import DetectionManager

import time, cv2

camera_configs = [
    {"id": "cam1", "type": "file", "path": "data/raw/sample.mp4"},
    {"id": "cam2", "type": "webcam", "index": 0},
    {"id": "mobile_cam","type": "mobile","url": "http://10.27.196.235:8080/video"},
]

cameras = [create_camera(cfg) for cfg in camera_configs]
manager = CameraManager(cameras)

dispatcher = FrameDispatcher(
    camera_ids=[cfg["id"] for cfg in camera_configs],
    buffer_size=20
)

fps = FPSController(target_fps=10)

detector = YOLOv8Detector("yolov8n.pt")
detect_mgr = DetectionManager(detector)

while True:
    packets = manager.read_all()

    for pkt in packets:
        frame_packet = FramePacket(
            camera_id=pkt["camera_id"],
            frame=pkt["frame"],
            timestamp=pkt["timestamp"]
        )
        dispatcher.push(frame_packet)

        synced_frames = dispatcher.pull_latest()

    for cam_id, pkt in synced_frames.items():
        det_pkt = detect_mgr.process(pkt)

        for det in det_pkt.detections:
            x1, y1, x2, y2 = map(int, det["bbox"])
            cv2.rectangle(pkt.frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow(cam_id, pkt.frame)

    fps.sync()


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



manager.release_all()
cv2.destroyAllWindows()
