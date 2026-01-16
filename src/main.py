from camera_layer.camera_factory import create_camera
from camera_layer.camera_manager import CameraManager
import cv2

camera_configs = [
    {
        "id": "cam1",
        "type": "file",
        "path": "data/raw/sample.mp4"
    },
    {
        "id": "cam2",
        "type": "webcam",
        "index": 0
    }
]

cameras = [create_camera(cfg) for cfg in camera_configs]
manager = CameraManager(cameras)

while True:
    packets = manager.read_all()

    for pkt in packets:
        frame = pkt["frame"]
        cam_id = pkt["camera_id"]

        cv2.imshow(cam_id, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

manager.release_all()
cv2.destroyAllWindows()
