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
        self.pred_batch_size = 16
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
        """Automatically batch and predict a numpy array of samples."""
        pred = []
        for i in tqdm(range(len(numpy_array) // self.pred_batch_size)):
            start = i * self.pred_batch_size
            end = (i + 1) * self.pred_batch_size
            in_tensor = torch.from_numpy(numpy_array[start:end]).to(torch.float32)
            pred.append(self.model(in_tensor).detach().numpy())
            del in_tensor

        if end < len(numpy_array):
            in_tensor = torch.from_numpy(numpy_array[end:]).to(torch.float32)
            pred.append(self.model(in_tensor).detach().numpy())
            del in_tensor

        return np.concatenate(pred, axis=0)
