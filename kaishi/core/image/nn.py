from torchvision import models
from torchvision import transforms
import pkg_resources
import torch
import torch.nn as nn


class Model:
    def __init__(self, n_classes=6, type='vgg16_bn'):
        """Initialize generic computer vision model class."""
        if type == 'vgg16_bn':
            self.model = self.vgg16_bn(n_classes)
            weights_filename = pkg_resources.resource_filename('kaishi', 'weights/image_macro_issues_vgg16.pth')
            gpu_flag = torch.cuda.is_available()
            if gpu_flag:
                state_dict = torch.load(weights_filename, map_location=torch.device('cuda'))
            else:
                state_dict = torch.load(weights_filename, map_location=torch.device('cpu'))
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
