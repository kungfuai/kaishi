"""Primary interface to the image tool kit."""
import os
from kaishi.core.image.file import ImageFileGroup


class Dataset(ImageFileGroup):
    """Primary object for image data sets."""
    def __init__(self, source=None): 

        ImageFileGroup.__init__(self)
        if source is not None:
            self.load_dir(source)

        # Define default pipeline
        self.pipeline = [self.filter_by_file_extension,
                         self.filter_invalid_image_headers,
                         self.filter_duplicates]
        self.pipeline_args = [[], [], []]
                         
        return

    def run_pipeline(self):
        """Run the full pipeline as configured."""
        for (pm, args) in zip(self.pipeline, self.pipeline_args):
            pm(*args)
