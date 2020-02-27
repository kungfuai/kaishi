"""Abstraction for PyTorch models."""
from torchvision import models
from torchvision import transforms
from tqdm import tqdm
import pkg_resources
import torch
import torch.nn as nn
import numpy as np


class Model:
    def __init__(self, n_classes: int = 6, model_arch: str = "resnet18"):
        """Initialize generic computer vision model class."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.batch_size = 16
        if model_arch == "vgg16_bn":
            self.model = self.vgg16_bn(n_classes)
            weights_filename = pkg_resources.resource_filename(
                "kaishi", "weights/image_macro_issues_vgg16.pth"
            )
        elif model_arch == "resnet18":
            self.model = self.resnet18(n_classes)
            weights_filename = pkg_resources.resource_filename(
                "kaishi", "weights/image_macro_issues_resnet18.pth"
            )
        elif model_arch == "resnet50":
            self.model = self.resnet50(n_classes)
            weights_filename = pkg_resources.resource_filename(
                "kaishi", "weights/image_macro_issues_resnet50.pth"
            )
        state_dict = torch.load(weights_filename, map_location=self.device)
        self.model.load_state_dict(state_dict)

    def vgg16_bn(self, n_classes: int):
        """Basic VGG16 model with specified number of output classes."""
        model = models.vgg16_bn(pretrained=False)  # PyTorch VGG16

        # Terminate with a custom number of classes
        n_inputs = model.classifier[-1].in_features
        model.classifier[6] = nn.Sequential(
            nn.Linear(n_inputs, 256),
            nn.ReLU(),
            nn.Dropout(0.15),
            nn.Linear(256, n_classes),
            nn.Sigmoid(),
        )

        return model

    def resnet18(self, n_classes: int):
        """Basic ResNet18 model with specified number of output classes."""
        model = torch.hub.load("pytorch/vision:v0.4.2", "resnet18", pretrained=False)
        model.fc = nn.Sequential(nn.Linear(512, n_classes), nn.Sigmoid())

        return model

    def resnet50(self, n_classes: int):
        """Basic ResNet50 with specified number of output classes."""
        model = torch.hub.load("pytorch/vision:v0.4.2", "resnet50", pretrained=False)
        model.fc = torch.nn.Sequential(
            torch.nn.Linear(in_features=2048, out_features=n_classes),
            torch.nn.Sigmoid(),
        )

        return model

    def predict(self, numpy_array):
        """Make predictions from a numpy array."""
        in_tensor = torch.from_numpy(numpy_array).to(torch.float32).to(self.device)

        return self.model(in_tensor).detach().cpu().numpy()
