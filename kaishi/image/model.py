"""Definition for PyTorch model abstraction."""
from torchvision import models
import pkg_resources
import torch
import torch.nn as nn


class Model:
    """Abstraction for working with PyTorch models."""

    def __init__(self, n_classes: int = 6, model_arch: str = "resnet18"):
        """Initialize generic computer vision model class.

        :param n_classes: number of classes at output layer
        :type n_classes: int
        :param model_arch: one of "resnet18", "vgg16_bn", or "resnet50"
        :type model_arch: str
        """
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
        """Basic VGG16 model with variable number of output classes.

        :param n_classes: number of classes at output layer
        :type n_classes: int
        :return: PyTorch VGG16 model object with batch normalization
        :rtype: `torchvision.models.vgg16_bn`
        """
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
        """Basic ResNet18 model with specified number of output classes.

        :param n_classes: number of classes at the output layer
        :type n_classes: int
        :return: PyTorch ResNet18 model object
        :rtype: `torchvision.models.resnet18`
        """
        model = torch.hub.load("pytorch/vision:v0.4.2", "resnet18", pretrained=False)
        model.fc = nn.Sequential(nn.Linear(512, n_classes), nn.Sigmoid())

        return model

    def resnet50(self, n_classes: int):
        """Basic ResNet50 model with specified number of output classes.

        :param n_classes: number of classes at the output layer
        :type n_classes: int
        :return: PyTorch ResNet50 model object
        :rtype: `torchvision.models.resnet50`
        """
        model = torch.hub.load("pytorch/vision:v0.4.2", "resnet50", pretrained=False)
        model.fc = torch.nn.Sequential(
            torch.nn.Linear(in_features=2048, out_features=n_classes),
            torch.nn.Sigmoid(),
        )

        return model

    def predict(self, numpy_array):
        """Make predictions from a numpy array, where dimensions are (batch, channel, x, y).

        :param numpy_array: input array to predict
        :type numpy_array: `numpy.array`
        :return: predictions, where the dimensions are (batch, output)
        :rtype: `numpy.array`
        """
        in_tensor = torch.from_numpy(numpy_array).to(torch.float32).to(self.device)

        return self.model(in_tensor).detach().cpu().numpy()
