from typing import List, Dict, Tuple
import os
from PIL import Image
import torch
from torch.utils.data import DataLoader
from torch import nn
from app.models import get_encoder, load_model, resnet50_transform
import pytest

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

class Dataset(torch.utils.data.Dataset):
    """

    """
    def __init__(self, dataset_path:str, encoder:Dict[str, int], transform=None):
        self.dataset_path = dataset_path
        self.encoder = encoder
        self.transform = transform
        
        self.dataset: List[Tuple[str, str]] = [] # list of pairs, each pair contains (image path, label name)

        for folder in os.listdir(dataset_path):
            folder_path = os.path.join(dataset_path, folder)
            images = os.listdir(folder_path)
            for image in images:
                if image.endswith(SUPPORTED_EXTENSIONS):
                    self.dataset.append((os.path.join(folder_path,image),folder))

    def __len__(self):
        return len(self.dataset)
    def __getitem__(self, idx):
        image_path = self.dataset[idx][0]
        label = self.dataset[idx][1]
        image =  Image.open(image_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, self.encoder[label]



def evaluate_model(model:nn.Module, test_loader,threshold:float, margin:float = 0.03):
    """
    Evaluates the model's performance on a test dataset using accuracy and loss.

    Parameters:
    -----------
    model : nn.Module
        The PyTorch model to evaluate.
    test_loader : DataLoader
        DataLoader object for the test dataset, assumed to return outputs in indices (not one-hot encoded).
    threshold: float
        The minimum accuracy threshold required.
    margin: float
         The acceptable deviation below the threshold within which the model’s accuracy 
    Returns:
    --------
    None

    Raises:
    -------
    AssertionError:
        If the model accuracy falls below the specified margin_accuracy.
    """
    loss_fn = nn.CrossEntropyLoss()
    correct_pred = 0
    total = len(test_loader)
    test_loss = 0
    with torch.no_grad():
        for inputs, outputs in test_loader:
            inputs, outputs = inputs.to(device), outputs.to(device)

            # Get model predictions
            preds = model(inputs)
            pred_indicies = torch.argmax(preds, dim=1)  # Get indices of the predictions

            # Calculate metrics
            total += len(outputs)
            correct_pred += (pred_indicies == outputs).sum().item()
            loss = loss_fn(preds, outputs)
            test_loss += loss.item()

    # Calculate accuracy
    accuracy = 100 * correct_pred / total
    print(f"Test Loss: {test_loss / len(test_loader):.4f}, Accuracy: {accuracy:.2f}%")

    assert accuracy >= (threshold - margin), (
        f"Model accuracy {accuracy:.2f}% is below the threshold of {(threshold-margin)* 100}%"
    )

@pytest.mark.parametrize("fruit_type, dataset_path,threshold", [
    ("banana", "test/dataset/banana",0.8),
 ])
def test_models(fruit_type:str,dataset_path:str, threshold:float):
    model = load_model(fruit_type,device)
    encoder = get_encoder(fruit_type)
    dataset = Dataset(dataset_path,encoder, resnet50_transform)
    loader = DataLoader(dataset, batch_size=32)
    evaluate_model(model, loader,threshold)
