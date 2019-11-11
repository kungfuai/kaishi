"""Primary interface to the image tool kit."""
import os
from kaishi.core.image.file import ImageFileGroup
from kaishi.util.pipeline import Pipeline


class Dataset(ImageFileGroup):
    """Primary object for image data sets."""
    PERCEPTUAL_HASH_THRESHOLD = 8  # Empirically determined, can be overridden in DEFUALT_PIPELINE_ARGS

    def __init__(self, source=None): 
        """Initialize with the default pipeline defined."""
        ImageFileGroup.__init__(self)
        if source is not None:
            self.load_dir(source)

        # Define default pipeline
        DEFAULT_PIPELINE_METHODS = [self.filter_invalid_file_extensions,
                                    self.filter_invalid_image_headers,
                                    self.filter_near_duplicates]
        DEFAULT_PIPELINE_ARGS = [[], [], [self.PERCEPTUAL_HASH_THRESHOLD]]
        self.pipeline = Pipeline(DEFAULT_PIPELINE_METHODS, DEFAULT_PIPELINE_ARGS)
                         
        return

    def run_pipeline(self, verbose=False):
        """Run the pipeline as configured."""
        self.pipeline.run(verbose)
        if verbose:
            print('Pipeline completed')

        return
