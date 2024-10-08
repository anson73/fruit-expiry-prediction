from typing import List, Tuple
from fastapi import FastAPI, UploadFile
from PIL import Image
import torch
from torchvision.transforms import v2
from torchvision import models
import io
from ultralytics import YOLO
import torchvision.transforms.functional as TF
import numpy as np


# Initialize FastAPI
app = FastAPI()

BANANA_LABELS = {
    0:"1-4 days",
    1:"5-9 days",
    2:"10-14 days",
    3:"expired",
}

STRAWBERRY_LABELS = {
    0: "1-2 days", 
    1: "3-5 days",
    2: "5-7 days",
    3:"7-10 days",
    4: "expired"
}

DETECTION_LABELS = {
    0: 'Apple',
    1: 'Banana',
    2: 'Grapes',
    3: 'Orange',
    4: 'Strawberry'
}


DETECTION_CONFIDENCE_THRESHOLD = 0.5

detector = YOLO("models/fruit_detection2.pt")

banana_predict = models.resnet50()
banana_predict.fc = torch.nn.Linear(banana_predict.fc.in_features, len(BANANA_LABELS))
banana_predict.load_state_dict(torch.load("../models/banana_resnet50.pth", map_location=torch.device('cpu')))
banana_predict.eval()

strawberry_predict = models.inception_v3()
strawberry_predict.fc = torch.nn.Linear(strawberry_predict.fc.in_features,len(STRAWBERRY_LABELS))
strawberry_predict.load_state_dict(torch.load("../models/strawberry_Inception.pth"))
strawberry_predict.eval()

resnet50_transform = v2.Compose([
    v2.Resize((256, 256)),
    v2.ToImageTensor(), 
    v2.ConvertImageDtype(),
    v2.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

inceptionv3_transform = v2.Compose([
    v2.Resize((299,299)),
    v2.ToImageTensor(), 
    v2.ConvertImageDtype(),
    v2.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),

])


def predict_banana(image:Image) -> str:
    img = inceptionv3_transform(img).unsqueeze(0)
    img = img.to(torch.device('cpu'))

    with torch.no_grad():
        output = banana_predict(img)
    predicted_class = output.argmax().item()
    return BANANA_LABELS[predicted_class]

def predict_strawberry(image:Image) -> str:
    img = inceptionv3_transform(img).unsqueeze(0)
    img = img.to(torch.device('cpu'))

    with torch.no_grad():
        output = strawberry_predict(img)
    predicted_class = output.argmax().item()
    return STRAWBERRY_LABELS[predicted_class]

def crop_image(image:Image,box:Tuple[int,int,int,int]):
    x1,y1,x2,y2 = box
    width = x2 - x1
    height = y2 - y1
    return TF.crop(image,y1,x1,height,width)

@app.post("/predict")
async def predict(file:UploadFile):
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
            cropped_images.append(crop_image(image,box),detected_class)
    prediction = ""
    for (cropped_image, detected_class) in cropped_images:
        if detected_class == 0:
            pass
        elif detected_class == 1:
            prediction = banana_predict(cropped_image)
    
    return {'prediction' :prediction}
