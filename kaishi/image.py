"""Primary interface to the image tool kit."""
import os
from kaishi.core.image.file import ImageFileGroup
from kaishi.util.pipeline import Pipeline
import warnings
import torch


class Dataset(ImageFileGroup):
    """Primary object for image data sets."""
    PERCEPTUAL_HASH_THRESHOLD = 3  # Empirically determined, can be overridden in DEFUALT_PIPELINE_ARGS

    def __init__(self, source=None):
        """Initialize with the default pipeline defined."""
        ImageFileGroup.__init__(self)
        if source is not None:
            self.load_dir(source)

        #
        if torch.cuda.is_available() is False:
            warnings.warn('No GPU detected, ConvNet prediction tasks will be very slow')
        # Define default pipeline
        """
        DEFAULT_PIPELINE_METHODS = [self.filter_invalid_file_extensions,
                                    self.filter_invalid_image_headers,
                                    self.filter_duplicates,
                                    self.filter_similar,
                                    self.collapse_children]
        """
        DEFAULT_PIPELINE_METHODS = [self.filter_invalid_file_extensions,
                                    self.filter_invalid_image_headers,
                                    self.filter_duplicates,
                                    self.collapse_children]
        #DEFAULT_PIPELINE_ARGS = [[], [], [], [self.PERCEPTUAL_HASH_THRESHOLD], []]
        DEFAULT_PIPELINE_ARGS = [[], [], [], []]
        self.pipeline = Pipeline(DEFAULT_PIPELINE_METHODS, DEFAULT_PIPELINE_ARGS)

        return

    def run_pipeline(self, verbose=False):
        """Run the pipeline as configured."""
        self.load_all()
        self.pipeline.run(verbose)
        if verbose:
            print('Pipeline completed')

        return
