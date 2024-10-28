import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
from typing import Dict, Tuple

# Labels for each fruit type
APPLE_LABELS = {0: "1-5 days", 1: "5-10 days", 2: "10-15 days", 3: "expired"}
BANANA_LABELS = {0: "1-4 days", 1: "5-9 days", 2: "10-14 days", 3: "expired"}
STRAWBERRY_LABELS = {0: "1-2 days", 1: "3-5 days", 2: "5-7 days", 3: "7-10 days", 4: "expired"}

# Model setup for each fruit type
# Apple model
apple_model = models.resnet50()
apple_model.fc = torch.nn.Linear(apple_model.fc.in_features, len(APPLE_LABELS))
apple_model.load_state_dict(torch.load("models/apple_resnet50.pth"))
apple_model.eval()

# Banana model
banana_model = models.resnet50()
banana_model.fc = torch.nn.Linear(banana_model.fc.in_features, len(BANANA_LABELS))
banana_model.load_state_dict(torch.load("models/banana_resnet50.pth"))
banana_model.eval()

# Strawberry model
strawberry_model = models.inception_v3()
strawberry_model.fc = torch.nn.Linear(strawberry_model.fc.in_features, len(STRAWBERRY_LABELS))
strawberry_model.load_state_dict(torch.load("models/strawberry_Inception.pth"))
strawberry_model.eval()

# Image transformations for each model type
resnet50_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

inceptionv3_transform = transforms.Compose([
    transforms.Resize((299, 299)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Predict shelf life based on detected fruit class
def predict_fruit_shelf_life(cropped_image: Image.Image, fruit_class: int) -> Dict[str, str | float]:
    if fruit_class == 0:
        return predict_shelf_life(cropped_image, apple_model, resnet50_transform, APPLE_LABELS, "apple")
    elif fruit_class == 1:
        return predict_shelf_life(cropped_image, banana_model, resnet50_transform, BANANA_LABELS, "banana")
    elif fruit_class == 4:
        return predict_shelf_life(cropped_image, strawberry_model, inceptionv3_transform, STRAWBERRY_LABELS, "strawberry")
    return {"fruit": "unknown", "prediction": "N/A", "confidence": 0}

# General function to make a prediction using a specified model and transformations
def predict_shelf_life(
    image: Image.Image,
    model: torch.nn.Module,
    transform,
    labels: Dict[int, str],
    fruit_type: str
) -> Dict[str, str | float]:
    # Transform the image
    img_tensor = transform(image).unsqueeze(0)
    model.eval()

    # Run prediction without gradient tracking
    with torch.no_grad():
        output = model(img_tensor)
        probabilities = F.softmax(output, dim=1)
        top_prob, top_idx = torch.max(probabilities, dim=1)
        predicted_class = top_idx.item()
        confidence_score = top_prob.item()

    # Return structured prediction data
    return {
        "fruit": fruit_type,
        "prediction": labels[predicted_class],
        "confidence": confidence_score
    }
