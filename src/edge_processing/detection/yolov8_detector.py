import torch
from ultralytics import YOLO

class YOLOv8Detector:
    def __init__(self, model_path="yolov8n.pt", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = YOLO(model_path)
        self.model.to(self.device)

    def detect(self, frame):
        results = self.model(frame, device=self.device, verbose=False)[0]

        detections = []
        for box in results.boxes:
            detections.append({
                "bbox": box.xyxy[0].tolist(),
                "confidence": float(box.conf[0]),
                "class_id": int(box.cls[0]),
                "class_name": results.names[int(box.cls[0])]
            })

        return detections
