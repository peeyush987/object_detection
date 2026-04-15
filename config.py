MODEL_OPTIONS = {
    "YOLOv8n (Nano - Fastest)": "yolov8n.pt",
    "YOLOv8s (Small)": "yolov8s.pt",
    "YOLOv8m (Medium)": "yolov8m.pt",
    "YOLOv8l (Large)": "yolov8l.pt",
    "Custom Model (My Trained Model)": "best.pt"  

}

# Known object sizes in meters (for distance estimation)
KNOWN_OBJECT_SIZES = {
    "person": 1.7,
    "car": 4.5,
    "truck": 8.0,
    "bus": 10.0,
    "bicycle": 1.8,
    "motorcycle": 2.0,
    "dog": 0.6,
    "cat": 0.4,
    "chair": 0.8,
    "couch": 2.0,
    "tv": 1.0,
    "laptop": 0.35,
    "cell phone": 0.15,
    "bottle": 0.25,
    "cup": 0.1,
    "book": 0.25,
    "backpack": 0.5,
    "umbrella": 0.8,
    "handbag": 0.4,
    "suitcase": 0.7
}

# Default settings
DEFAULT_CONFIDENCE = 0.25
DEFAULT_DISTANCE_THRESHOLD = 10.0
DEFAULT_FOCAL_LENGTH = 700
DEFAULT_CAMERA_INDEX = 0
