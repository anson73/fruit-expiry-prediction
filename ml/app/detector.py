from ultralytics import YOLO
from typing import List, Tuple
from PIL import Image
import torchvision.transforms.functional as TF

DETECTION_CONFIDENCE_THRESHOLD = 0.5
detector = YOLO("app/models/fruit_detection.pt")

def detect_fruit(image: Image) -> List[Tuple[Image.Image, int]]:
    results = detector(image)
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    confidences = results[0].boxes.conf.tolist()
    return build_results(zip(boxes, classes, confidences), image)

def crop_image(image: Image, box: Tuple[int, int, int, int]) -> Image:
    x1, y1, x2, y2 = box
    width = x2 - x1
    height = y2 - y1
    return TF.crop(image, y1, x1, height, width)

def build_results(detections: zip, image: Image) -> List[Tuple[Image.Image, int]]:
    boxes, classes, confidences = zip(*detections)
    most_confident_class = get_most_confident_class(list(confidences), list(classes))
    
    detections = zip(boxes, classes, confidences)
    return filter_out(most_confident_class, detections, image)

def get_most_confident_class(confidences: List[float], classes: List[int]) -> int:
    max_confidence = max(confidences)
    max_index = confidences.index(max_confidence)
    return classes[max_index]

def filter_out(most_confident_class: int, detections: zip, image: Image) -> List[Tuple[Image.Image, int]]:
    detected_fruits = []
    for box, fruit_class, confidence in detections:
        if confidence > DETECTION_CONFIDENCE_THRESHOLD and fruit_class == most_confident_class:
            cropped_img = crop_image(image, box)
            detected_fruits.append((cropped_img, fruit_class))
    return detected_fruits
