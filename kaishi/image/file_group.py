"""Definition for groups of image files."""
import os
import numpy as np
from PIL import Image
from kaishi.core.file_group import FileGroup
from kaishi.image.util import swap_channel_dimension
from kaishi.image.file import ImageFile


THUMBNAIL_SIZE = (64, 64)
MAX_DIM_FOR_SMALL = 224  # Max dimension for small sample
PATCH_SIZE = (64, 64)  # Patch size for compression artifact detection
RESAMPLE_METHOD = Image.NEAREST  # Resampling method for resizing images


class ImageFileGroup(FileGroup):
    """Group of image files that inherits from the core file group class."""

    # Externally defined classes and methods
    from kaishi.image.generator import train_generator
    from kaishi.image.generator import generate_validation_data
    from kaishi.image.util import get_batch_dimensions
    from kaishi.image.filters.similar import FilterSimilar
    from kaishi.image.filters.invalid_file_extensions import FilterInvalidFileExtensions
    from kaishi.image.filters.invalid_image_headers import FilterInvalidImageHeaders
    from kaishi.image.labelers.generic_convnet import LabelerGenericConvnet
    from kaishi.image.transforms.fix_rotation import TransformFixRotation
    from kaishi.image.transforms.to_grayscale import TransformToGrayscale
    from kaishi.image.transforms.limit_dimensions import TransformLimitDimensions

    def __init__(self, source: str, recursive: bool):
        """Initialize new image file group.

        :param source: directory containing data
        :type source: str
        :param recursive: flag indicating recursion
        :type recursive: bool
        """
        super().__init__(recursive=recursive)
        self.thumbnail_size = THUMBNAIL_SIZE
        self.max_dim_for_small = MAX_DIM_FOR_SMALL
        self.patch_size = PATCH_SIZE
        self.model = None  # Only load model if needed
        self.labeled = False
        self.load_dir(source, ImageFile, recursive)

    def load_all(self):
        """Load all files in the directory that this class was initialized with."""
        for fobj in self.files:
            fobj.verify_loaded()

    def build_numpy_batches(
        self,
        channels_first: bool = True,
        batch_size: int = None,
        image_type: str = "small_image",
    ):
        """Build a tensor from the entire image corpus (or generate batches if specified).

        If a batch size is specified, this acts as a generator of batches and returns a list
        of file objects to manipulate. Otherwise, a single batch of all images is returned in an array format.

        :param channels_first: flag indicating channels first (e.g. PyTorch) vs. channels last (e.g. Keras)
        :type channels_first: bool
        :param batch_size: size of each batch (default is `None`, which will return a single batch)
        :type batch_size: int
        :param image_type: choice of "small_image", "thumbnail", or "patch", indicating which version of each image to use
        :type image_type: str
        :return: batch of images (generator if batch size specified)
        :rtype: `numpy.array`
        """
        final_batch_size = batch_size if batch_size is not None else len(self.files)
        shape = self.get_batch_dimensions(
            final_batch_size, channels_first=False, image_type=image_type
        )  # Start with PIL-style channel layout
        im_tensor = np.zeros(shape)

        bi = 0
        batch_file_objects = []
        for fobj in self.files:
            try:
                fobj.verify_loaded()
                if image_type == "small_image":
                    im_tensor[bi] = np.array(fobj.small_image.convert("RGB"))
                elif image_type == "thumbnail":
                    im_tensor[bi] = np.array(fobj.thumbnail.convert("RGB"))
                elif image_type == "patch":
                    im_tensor[bi] = np.array(fobj.patch.convert("RGB"))
            except AttributeError:
                continue
            bi += 1
            if batch_size is not None:
                batch_file_objects.append(fobj)
                if bi == batch_size:
                    if channels_first:
                        yield swap_channel_dimension(im_tensor), batch_file_objects
                    else:
                        yield im_tensor, batch_file_objects
                    bi = 0  # Reset the batch
                    batch_file_objects = []

        if batch_size is None:
            if channels_first:
                return swap_channel_dimension(im_tensor)
            return (
                im_tensor  # Don't return file objects as it's the same as 'self.files'
            )
        if channels_first:
            yield swap_channel_dimension(im_tensor), batch_file_objects
        else:
            yield im_tensor, batch_file_objects

    def save(self, out_dir: str):
        """Save image data set in the current structure while preserving any changes.

        :param out_dir: output directory
        :type out_dir: str
        """
        out_dir = os.path.abspath(out_dir)
        if not os.path.exists(out_dir):  # Ensure output directory exists
            os.makedirs(out_dir)
        for fobj in self.files:  # Determine file paths and save
            if fobj.image is None:
                continue
            if fobj.relative_path is not None:
                file_dir = os.path.join(out_dir, fobj.relative_path)
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
            else:
                file_dir = out_dir
            fobj.image.save(os.path.join(file_dir, fobj.basename))

    def run_pipeline(self, verbose: bool = False):
        """Run the pipeline as configured.

        :param verbose: flag indicating verbosity
        :type verbose: bool
        """
        self.load_all()
        self.pipeline(self, verbose=verbose)
        if verbose:
            print("Pipeline completed")

    def report(self):
        """Run a descriptive report (currently just prints the file report)."""
        self.file_report()
