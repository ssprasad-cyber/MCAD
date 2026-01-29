from camera_layer.camera_factory import create_camera
from camera_layer.camera_manager import CameraManager
from edge_processing.frame_capture.frame_packet import FramePacket
from edge_processing.frame_capture.frame_dispatcher import FrameDispatcher
from edge_processing.frame_capture.fps_controller import FPSController
import time, cv2

camera_configs = [
    {"id": "cam1", "type": "file", "path": "data/raw/sample.mp4"},
    {"id": "cam2", "type": "webcam", "index": 0}
]

cameras = [create_camera(cfg) for cfg in camera_configs]
manager = CameraManager(cameras)

dispatcher = FrameDispatcher(
    camera_ids=[cfg["id"] for cfg in camera_configs],
    buffer_size=20
)

fps = FPSController(target_fps=10)

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
        cv2.imshow(cam_id, pkt.frame)

    fps.wait()


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



manager.release_all()
cv2.destroyAllWindows()
