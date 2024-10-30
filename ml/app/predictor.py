import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
from typing import Dict
from app.cbam import add_cbam_into_resnet_bottlenecks
from torch import nn

apple_encoder = {0:'expired',1:'1-5',2:'6-10 days', 3:'11-15 days', 4:'16-20 days'}
banana_encoder = {0:'expired',1:'1-2 days',2:'3-4 days',3:'5-7 days', 4:'8-10 days'}
strawberry_encoder = {0:'expired',1:'1-2 days',2:'3-4 days',3:'5-7 days', 4:'8-10 days'}
mango_encoder = {0:'expired', 1:'1-2 days', 2:'3-6 days', 3:'7-10 days'}
orange_encoder = {0:'expired', 1:'0-1 days', 2:'2-5 days', 3:'6-9 days', 4:'10-14 days' }

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def create_resnet50_model(num_classes=5,seed=42):
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    # # freezing all layers
    # for param in model.parameters():
    #     param.requires_grad = False
    torch.manual_seed(seed)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(in_features=in_features,out_features=num_classes,bias=True)
    )
    return model

# Model setup for each fruit type
# Apple model
apple_model = create_resnet50_model(num_classes=len(apple_encoder))
apple_model = add_cbam_into_resnet_bottlenecks(apple_model,[1,2,3,4])
apple_model.load_state_dict(
    torch.load(
        f= "app/models/apple_model.pth",
        map_location=device,
        weights_only=True,
    )
)

# Banana model
banana_model = create_resnet50_model(num_classes=len(banana_encoder))
banana_model = add_cbam_into_resnet_bottlenecks(banana_model,[1,2,3,4])
banana_model.load_state_dict(
    torch.load(
        f= "app/models/banana_model.pth",
        map_location=device,
        weights_only=True,
    )
)

# orange model
orange_model = create_resnet50_model(num_classes=len(orange_encoder))
orange_model = add_cbam_into_resnet_bottlenecks(orange_model,[1,2,3,4])
orange_model.load_state_dict(
    torch.load(
        f = "app/models/orange_model.pth",
        map_location=device,
        weights_only=True,
    )
)
# Strawberry model
strawberry_model =create_resnet50_model(num_classes=len(strawberry_encoder))
strawberry_model = add_cbam_into_resnet_bottlenecks(strawberry_model,[1,2,3,4])
strawberry_model.load_state_dict(
    torch.load(
        f="app/models/strawberry_model.pth",
        map_location=device,
        weights_only=True,
    )
)

# mango model
mango_model = create_resnet50_model(num_classes=len(mango_encoder))
mango_model = add_cbam_into_resnet_bottlenecks(mango_model,[1,2,3,4])
mango_model.load_state_dict(
    torch.load(
        f= "app/models/mango_model.pth",
        map_location=device,
        weights_only=True,
    )
)



# Image transformations for each model type
resnet50_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Predict shelf life based on detected fruit class
def predict_fruit_shelf_life(cropped_image: Image.Image, fruit_class: int) -> Dict[str, str | float]:
    if fruit_class == 0:
        return predict_shelf_life(cropped_image, apple_model, resnet50_transform, apple_encoder, "apple")
    elif fruit_class == 1:
        return predict_shelf_life(cropped_image, banana_model, resnet50_transform, banana_encoder, "banana")
    elif fruit_class == 2:
        return predict_shelf_life(cropped_image,mango_model, resnet50_transform, mango_encoder, "mango")
    elif fruit_class == 3:
        return predict_shelf_life(cropped_image, orange_model, resnet50_transform, orange_encoder, "orange")
    elif fruit_class == 4:
        return predict_shelf_life(cropped_image, strawberry_model, resnet50_transform, strawberry_encoder, "strawberry")
    return {"fruit": "unknown", "prediction": "N/A", "confidence": 0}

# General function to make a prediction using a specified model and transformations
def predict_shelf_life(
    image: Image.Image,
    model: torch.nn.Module,
    transform,
    encoder: Dict[int, str],
    fruit_type: str
) -> Dict[str, str | float]:
    # Transform the image
    img_tensor = transform(image).unsqueeze(0)

    img_tensor = img_tensor.to(device)
    model = model.to(device)

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
        "prediction": encoder[predicted_class],
        "confidence": confidence_score
    }
