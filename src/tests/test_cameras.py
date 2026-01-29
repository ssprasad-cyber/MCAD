from camera_layer.camera_manager import CameraManager
from camera_layer.camera_factory import create_camera
import cv2

# ===== CHANGE ONLY THIS CONFIG =====
camera_configs = [
    # 1️⃣ Video file
    # {
    #     "id": "file_cam",
    #     "type": "file",
    #     "path": "/home/ssaiprasad/Downloads/fight.mp4"
    # },

    # 2️⃣ Laptop webcam
    # {
    #     "id": "webcam",
    #     "type": "webcam",
    #     "index": 0
    # },

    # 3️⃣ External USB webcam (try 1, 2 if needed)
    # {
    #     "id": "usb_cam",
    #     "type": "webcam",
    #     "index": 1
    # },

    # 4️⃣ Mobile camera (IP Webcam)
    {
        "id": "mobile_cam",
        "type": "mobile",
        "url": "http://10.27.196.235:8080/video"
    },

    # 5️⃣ RTSP CCTV
    # {
    #     "id": "rtsp_cam",
    #     "type": "rtsp",
    #     "url": "rtsp://username:password@ip:554/stream"
    # }
]

# ==================================

cameras = [create_camera(cfg) for cfg in camera_configs]
manager = CameraManager(cameras)

print("Press Q to exit")

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
