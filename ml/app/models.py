import torch
from torch import nn
from torchvision import models, transforms
from app.cbam import add_cbam_into_resnet_bottlenecks


apple_encoder = {0:'expired',1:'1-5',2:'6-10 days', 3:'11-15 days', 4:'16-20 days'}
banana_encoder = {0:'expired',1:'1-2 days',2:'3-4 days',3:'5-7 days', 4:'8-10 days'}
strawberry_encoder = {0:'expired',1:'1-2 days',2:'3-4 days',3:'5-7 days', 4:'8-10 days'}
mango_encoder = {0:'expired', 1:'1-2 days', 2:'3-6 days', 3:'7-10 days'}
orange_encoder = {0:'expired', 1:'0-1 days', 2:'2-5 days', 3:'6-9 days', 4:'10-14 days' }


model_info = {
     "apple": {"path": "app/models/apple_model.pth", "encoder": apple_encoder},
    "banana": {"path": "app/models/banana_model.pth", "encoder": banana_encoder},
    "orange": {"path": "app/models/orange_model.pth", "encoder": orange_encoder},
    "strawberry": {"path": "app/models/strawberry_model.pth", "encoder": strawberry_encoder},
    "mango": {"path": "app/models/mango_model.pth", "encoder": mango_encoder}
}

# Image transformations (shared across all models)
resnet50_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Create ResNet50 with a modified final layer
def create_resnet50_model(num_classes=5, seed=42):
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    torch.manual_seed(seed)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(in_features=in_features,out_features=num_classes,bias=True)
    )
    return model

# General model setup and loading function
def load_model(fruit_type:str, device:torch.device):
    """
    """
    model_path = model_info[fruit_type]["path"]
    encoder = model_info[fruit_type]["encoder"]
    model = create_resnet50_model(num_classes=len(encoder))
    model = add_cbam_into_resnet_bottlenecks(model, [1,2,3,4])
    model.load_state_dict(
        torch.load(model_path, map_location=device)
    )
    model.to(device)
    model.eval()  # Set the model to evaluation mode
    return model, encoder
