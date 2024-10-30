from ultralytics import YOLO
from typing import List, Tuple
from PIL import Image
import torchvision.transforms.functional as TF

DETECTION_CONFIDENCE_THRESHOLD = 0.5
detector = YOLO("app/models/sprint1_detection_model.pt")

def detect_fruit(image: Image) -> List[Tuple[Image.Image, int]]:
    results = detector(image)
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    confidences = results[0].boxes.conf.tolist()

    # Only process detections that pass the confidence threshold
    detected_fruits = []
    for box, fruit_class, confidence in zip(boxes, classes, confidences):
        if confidence > DETECTION_CONFIDENCE_THRESHOLD:
            cropped_img = crop_image(image, box)
            detected_fruits.append((cropped_img, fruit_class))
    
    return detected_fruits

def crop_image(image: Image, box: Tuple[int, int, int, int]) -> Image:
    x1, y1, x2, y2 = box
    width = x2 - x1
    height = y2 - y1
    return TF.crop(image, y1, x1, height, width)
