"""Definitions for image file objects and groups of them."""
import os
import multiprocessing
import numpy as np
from PIL import Image
import imagehash
from kaishi.core.file import File, FileGroup
from kaishi.core.misc import load_files_by_walk
from kaishi.image.util import swap_channel_dimension
from kaishi.image import ops


THUMBNAIL_SIZE = (64, 64)
MAX_DIM_FOR_SMALL = 224  # Max dimension for small sample
PATCH_SIZE = (64, 64)  # Patch size for compression artifact detection
RESAMPLE_METHOD = Image.NEAREST  # Resampling method for resizing images
VALID_EXT = [
    ".bmp",
    ".dib",
    ".jpeg",
    ".jpg",
    ".jpe",
    ".jp2",
    ".png",
    ".pbm",  # Valid image extensions
    ".pgm",
    ".ppm",
    ".sr",
    ".ras",
    ".tiff",
    ".tif",
]


class ImageFile(File):
    """Class extension from 'File' for image-specific attributes and methods."""

    def __init__(self, basedir: str, relpath: str, filename: str):
        """Add members to supplement File class."""
        File.__init__(self, basedir, relpath, filename)
        self.children["similar"] = []
        self.image = None
        self.small_image = None
        self.thumbnail = None
        self.patch = None
        self.perceptual_hash = None

    def verify_loaded(self):
        """Verify image and derivatives are loaded (only loading when necessary)."""
        if self.image is None:
            try:
                self.image = Image.open(self.abspath)
                self.image.load()  # https://github.com/python-pillow/Pillow/issues/1144
                self.thumbnail = self.image.resize(THUMBNAIL_SIZE)
                self.small_image = ops.make_small(
                    self.image,
                    max_dim=MAX_DIM_FOR_SMALL,
                    resample_method=RESAMPLE_METHOD,
                )
                self.patch = ops.extract_patch(self.image, PATCH_SIZE)
            except OSError:  # Not an image file
                self.image = None

    def rotate(self, ccw_rotation_degrees: int):
        """Rotate all instances of image by 'ccw_rotation_degrees'."""
        self.image = self.image.rotate(ccw_rotation_degrees, expand=True)
        self.thumbnail = self.thumbnail.rotate(ccw_rotation_degrees, expand=True)
        self.small_image = self.small_image.rotate(ccw_rotation_degrees, expand=True)
        self.patch = self.patch.rotate(ccw_rotation_degrees, expand=True)

    def compute_perceptual_hash(self, hashfunc=imagehash.average_hash):
        """Calculate perceptual hash (close in value to similar images."""
        self.verify_loaded()
        if self.image is None:  # Couldn't load the image
            return None

        self.perceptual_hash = hashfunc(self.thumbnail)

        return self.perceptual_hash


class ImageFileGroup(FileGroup):
    """Class to operate on an image file group."""

    # Externally defined classes and methods
    from kaishi.image.generator import train_generator
    from kaishi.image.generator import generate_validation_data
    from kaishi.image.util import get_batch_dimensions
    from kaishi.image.filters import FilterSimilar
    from kaishi.image.filters import FilterInvalidFileExtensions
    from kaishi.image.filters import FilterInvalidImageHeaders
    from kaishi.image.labelers import LabelerMacro
    from kaishi.image.transforms import TransformFixRotation

    def __init__(self):
        """Initialize new image file group."""
        FileGroup.__init__(self)
        self.thumbnail_size = THUMBNAIL_SIZE
        self.max_dim_for_small = MAX_DIM_FOR_SMALL
        self.patch_size = PATCH_SIZE
        self.valid_ext = VALID_EXT
        self.model = None  # Only load model if needed
        self.labeled = False

    def load_dir(self, dir_name: str):
        """Read file names in a directory while ignoring subdirectories."""
        self.dir_name, self.dir_children, self.files = load_files_by_walk(
            dir_name, ImageFile
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
