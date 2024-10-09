import torch
import torchvision
from torchvision import models

apple_predict = models.resnet50()
apple_predict.load_state_dict(torch.load('apple_resnet50.pth'))

apple_predict.names
