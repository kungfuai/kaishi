"""Primary interface to the image tool kit."""
import os
import warnings
from kaishi.image.file_group import ImageFileGroup
import torch


class ImageDataset:
    """Factory for image dataset objects."""

    def __new__(self, source: str = None, recursive: bool = False):
        """Initialize with the default pipeline defined."""
        if torch.cuda.is_available() is False:
            warnings.warn("No GPU detected, ConvNet prediction tasks will be very slow")

        if os.path.exists(source):
            return ImageFileGroup(source=source, recursive=recursive)
        else:
            raise NotImplementedError("Currently only supports a valid path as input")
