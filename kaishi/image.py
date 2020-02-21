"""Primary interface to the image tool kit."""
import os
from kaishi.core.image.file import ImageFileGroup
from kaishi.util.pipeline import Pipeline
import warnings
import torch


class Dataset(ImageFileGroup):
    """Primary object for image data sets."""

    PERCEPTUAL_HASH_THRESHOLD = (
        3  # Empirically determined, can be overridden in DEFUALT_PIPELINE_ARGS
    )

    def __init__(self, source=None):
        """Initialize with the default pipeline defined."""
        ImageFileGroup.__init__(self)
        if source is not None:
            if os.path.exists(source):
                self.load_dir(source)
            else:
                warnings.warn("Directory not found, initializing empty Dataset")

        # Make sure GPU is available, warn if not
        if torch.cuda.is_available() is False:
            warnings.warn("No GPU detected, ConvNet prediction tasks will be very slow")

        # self.pipeline = Pipeline(DEFAULT_PIPELINE_METHODS, DEFAULT_PIPELINE_ARGS)

        return

    def run(self, pool=False, verbose=False):
        """Run the pipeline as configured."""
        self.load_all(pool=pool)
        self.pipeline(self, verbose=verbose)
        if verbose:
            print("Pipeline completed")

        return
