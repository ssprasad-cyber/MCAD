from .file_camera import FileCamera
from .webcam_camera import WebcamCamera
from .mobile_camera import MobileCamera
from .rtsp_camera import RTSPCamera

def create_camera(cfg):
    cam_type = cfg["type"]

    if cam_type == "file":
        return FileCamera(cfg["id"], cfg["path"])

    if cam_type == "webcam":
        return WebcamCamera(cfg["id"], cfg.get("index", 0))

    if cam_type == "mobile":
        return MobileCamera(cfg["id"], cfg["url"])

    if cam_type == "rtsp":
        return RTSPCamera(cfg["id"], cfg["url"])

    raise ValueError(f"Unknown camera type: {cam_type}")
