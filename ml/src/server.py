from typing import List, Tuple, Optional, Dict
from fastapi import FastAPI, UploadFile
from PIL import Image
import torch
from torchvision.transforms import v2
from torchvision import models
import io
from ultralytics import YOLO
import torchvision.transforms.functional as TF
import torch.nn.functional as F

# Initialize FastAPI
app = FastAPI()

BANANA_LABELS = {
    0: "1-4 days",
    1: "5-9 days",
    2: "10-14 days",
    3: "expired",
}

STRAWBERRY_LABELS = {
    0: "1-2 days",
    1: "3-5 days",
    2: "5-7 days",
    3: "7-10 days",
    4: "expired"
}

APPLE_LABELS = {
    0: "1-5",
    1: "5-10",
    2: "10-15",
    3: "expired"
}

DETECTION_LABELS = {
    0: 'Apple',
    1: 'Banana',
    2: 'Mango',
    3: 'Orange',
    4: 'Strawberry'
}

DETECTION_CONFIDENCE_THRESHOLD = 0.5

detector = YOLO("../models/sprint1_detection_model.pt")

banana_predict = models.resnet50()
banana_predict.fc = torch.nn.Linear(banana_predict.fc.in_features, len(BANANA_LABELS))
banana_predict.load_state_dict(torch.load("../models/banana_resnet50.pth", map_location=torch.device('cpu')))
banana_predict.eval()

apple_predict = models.resnet50()
apple_predict.fc = torch.nn.Linear(apple_predict.fc.in_features, len(APPLE_LABELS))
apple_predict.load_state_dict(torch.load("../models/apple_resnet50.pth", map_location=torch.device('cpu')))
apple_predict.eval()

strawberry_predict = models.inception_v3()
strawberry_predict.fc = torch.nn.Linear(strawberry_predict.fc.in_features, len(STRAWBERRY_LABELS))
strawberry_predict.load_state_dict(torch.load("../models/strawberry_Inception.pth"))
strawberry_predict.eval()

resnet50_transform = v2.Compose([
    v2.Resize((256, 256)),
    v2.Pad((0, 0, 256, 256)),
    v2.ToImageTensor(),
    v2.ConvertImageDtype(),
    v2.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

inceptionv3_transform = v2.Compose([
    v2.Resize((299, 299)),
    v2.Pad((0, 0, 299, 299)),
    v2.ToImageTensor(),
    v2.ConvertImageDtype(),
    v2.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),

])


def predict_shelf_life(
        image: Image.Image,
        model: torch.nn.Module,
        transform,
        labels: Dict[int, str],
        device: Optional[str] = 'cpu'
) -> Tuple[str, float]:
    img_tensor = transform(image).unsqueeze(0).to(device)
    model.to(device)
    model.eval()

    with torch.no_grad():
        output = model(img_tensor)
        probabilities = F.softmax(output, dim=1)
        top_prob, top_idx = torch.max(probabilities, dim=1)
        predicted_class = top_idx.item()
        confidence_score = top_prob.item()

    predicted_label = labels[predicted_class]

    return predicted_label, confidence_score


def crop_image(image: Image, box: Tuple[int, int, int, int]):
    x1, y1, x2, y2 = box
    width = x2 - x1
    height = y2 - y1
    return TF.crop(image, y1, x1, height, width)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(file: UploadFile):
    image = Image.open(io.BytesIO(await file.read()))
    # convert image to rgb format
    if image.mode != 'RGB':
        image = image.convert('RGB')

    results = detector(image)

    cropped_images = []

    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    confidences = results[0].boxes.conf.tolist()

    # Iterate through the results
    for box, detected_class, confidence in zip(boxes, classes, confidences):
        if confidence > DETECTION_CONFIDENCE_THRESHOLD:
            cropped_images.append((crop_image(image, box), detected_class))
    prediction = ""
    fruit_detected = "no fruit detected"
    conf_score = 0
    for (cropped_image, detected_class) in cropped_images:
        if detected_class == 0:
            prediction, conf_score = predict_shelf_life(cropped_image, apple_predict, resnet50_transform, APPLE_LABELS)
            fruit_detected = "apple"
        elif detected_class == 1:
            prediction, conf_score = predict_shelf_life(cropped_image, banana_predict, resnet50_transform,
                                                        BANANA_LABELS)
            fruit_detected = "banana"
        elif detected_class == 2:
            fruit_detected = "mango"
        elif detected_class == 3:
            fruit_detected = "orange"
        elif detected_class == 4:
            prediction, conf_score = predict_shelf_life(cropped_image, strawberry_predict, inceptionv3_transform,
                                                        STRAWBERRY_LABELS)
            fruit_detected = "strawberry"

    return {'prediction': prediction, 'fruit_detected': fruit_detected, 'confidence': conf_score}
