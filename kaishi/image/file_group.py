"""Definitions for image file objects and groups of them."""
import os
import multiprocessing
import numpy as np
from PIL import Image
from kaishi.core.file import File
from kaishi.core.file_group import FileGroup
from kaishi.core.misc import load_files_by_walk
from kaishi.image.util import swap_channel_dimension
from kaishi.image import ops
from kaishi.image.file import ImageFile


THUMBNAIL_SIZE = (64, 64)
MAX_DIM_FOR_SMALL = 224  # Max dimension for small sample
PATCH_SIZE = (64, 64)  # Patch size for compression artifact detection
RESAMPLE_METHOD = Image.NEAREST  # Resampling method for resizing images


class ImageFileGroup(FileGroup):
    """Class to operate on an image file group."""

    # Externally defined classes and methods
    from kaishi.image.generator import train_generator
    from kaishi.image.generator import generate_validation_data
    from kaishi.image.util import get_batch_dimensions
    from kaishi.image.filters.similar import FilterSimilar
    from kaishi.image.filters.invalid_file_extensions import FilterInvalidFileExtensions
    from kaishi.image.filters.invalid_image_headers import FilterInvalidImageHeaders
    from kaishi.image.labelers.generic_convnet import LabelerGenericConvnet
    from kaishi.image.transforms.fix_rotation import TransformFixRotation

    def __init__(self, recursive: bool):
        """Initialize new image file group."""
        super().__init__(recursive=recursive)
        self.thumbnail_size = THUMBNAIL_SIZE
        self.max_dim_for_small = MAX_DIM_FOR_SMALL
        self.patch_size = PATCH_SIZE
        self.model = None  # Only load model if needed
        self.labeled = False

    def load_dir(self, dir_name: str):
        """Read file names in a directory while ignoring subdirectories."""
        self.dir_name, self.dir_children, self.files = load_files_by_walk(
            dir_name, ImageFile, recursive=self.recursive
        )

    def load_instance(self, fobj):
        """Method to load an image object."""
        fobj.verify_loaded()

    def load_all(self, pool: bool = True):
        """Load all files. If 'pool' is True, a multiprocessing pool is used."""
        if pool:
            pool = multiprocessing.Pool(multiprocessing.cpu_count())
            pool.map(self.load_instance, self.files)
        else:
            for fobj in self.files:
                self.load_instance(fobj)

    def build_numpy_batches(
        self,
        channels_first: bool = True,
        batch_size: int = None,
        image_type: str = "small_image",
    ):
        """Build a tensor from the entire image corpus (or generate batches if specified).

        If a batch size is specified, this acts as a generator of batches and returns a list
        of file objects to manipulate.

        'channels_first' - 'True' if channels are the first dimension (standard for PyTorch)
        'image_type' is one of 'thumbnail', 'small_image', or 'patch'
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
        """Save image data set in the same structure while preserving any changes."""
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
