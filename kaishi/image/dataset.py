"""Primary interface to the image tool kit."""
import os
import warnings
from kaishi.image.file import ImageFileGroup
import torch


class ImageDataset(ImageFileGroup):
    """Primary object for image data sets."""

    def __init__(self, source: str = None, recursive: bool = False):
        """Initialize with the default pipeline defined."""
        super().__init__(recursive=recursive)
        if source is not None:
            if os.path.exists(source):
                self.load_dir(source)
            else:
                warnings.warn("Directory not found, initializing empty Dataset")

        # Make sure GPU is available, warn if not
        if torch.cuda.is_available() is False:
            warnings.warn("No GPU detected, ConvNet prediction tasks will be very slow")

    def run_pipeline(self, pool: bool = False, verbose: bool = False):
        """Run the pipeline as configured."""
        self.load_all(pool=pool)
        self.pipeline(self, verbose=verbose)
        if verbose:
            print("Pipeline completed")

    def report(self):
        """Run a descriptive report."""
        self.file_report()
