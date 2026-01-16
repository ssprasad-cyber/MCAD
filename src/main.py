from camera_layer.camera_factory import create_camera
from camera_layer.camera_manager import CameraManager
from edge_processing.frame_capture.frame_buffer import FrameBuffer
from edge_processing.frame_capture.fps_controller import FPSController
import cv2

camera_configs = [
    {"id": "cam1", "type": "file", "path": "data/raw/sample.mp4"},
    {"id": "cam2", "type": "webcam", "index": 0}
]

cameras = [create_camera(cfg) for cfg in camera_configs]
manager = CameraManager(cameras)

buffers = {
    cam.camera_id: FrameBuffer(max_size=20)
    for cam in cameras
}

fps_ctrl = FPSController(target_fps=10)

while True:
    packets = manager.read_all()

    # Push into buffers
    for pkt in packets:
        buffers[pkt["camera_id"]].push(pkt)

    # Controlled pop (simulate next stage)
    for cam_id, buffer in buffers.items():
        frame_pkt = buffer.latest()
        if frame_pkt:
            cv2.imshow(cam_id, frame_pkt["frame"])

    fps_ctrl.wait()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

manager.release_all()
cv2.destroyAll()
