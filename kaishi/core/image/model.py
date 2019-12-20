from torchvision import models
from torchvision import transforms
from tqdm import tqdm
import pkg_resources
import torch
import torch.nn as nn
import numpy as np


class Model:
    def __init__(self, n_classes=6, type='vgg16_bn'):
        """Initialize generic computer vision model class."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.batch_size = 16
        if type == 'vgg16_bn':
            self.model = self.vgg16_bn(n_classes)
            weights_filename = pkg_resources.resource_filename('kaishi', 'weights/image_macro_issues_vgg16.pth')
            state_dict = torch.load(weights_filename, map_location=self.device)
            self.model.load_state_dict(state_dict)

        return

    def vgg16_bn(self, n_classes):
        """Basic VGG16 model in PyTorch with specified number of output classes."""
        model = models.vgg16_bn(pretrained=False)  # PyTorch VGG16

        # Terminate with a custom number of classes
        n_inputs = model.classifier[-1].in_features
        model.classifier[6] = nn.Sequential(nn.Linear(n_inputs, 256),
                                            nn.ReLU(),
                                            nn.Dropout(0.15),
                                            nn.Linear(256, n_classes),
                                            nn.Sigmoid())

        return model

    def predict(self, numpy_array):
        """Make predictions from a numpy array."""
        in_tensor = torch.from_numpy(numpy_array).to(torch.float32).to(self.device)

        return self.model(in_tensor).detach().cpu().numpy()