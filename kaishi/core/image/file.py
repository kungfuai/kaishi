import os
import copy
import numpy as np
import imghdr
from PIL import Image
import imagehash
from tqdm import tqdm
from kaishi.util.file import File, FileGroup
from kaishi.util.misc import load_files_by_walk
from kaishi.core.image.util import swap_channel_dimension
from sklearn.feature_extraction.image import extract_patches_2d


THUMBNAIL_SIZE = (64, 64)
MAX_DIM_FOR_SMALL = 224  # Max dimension for small sample
PATCH_SIZE = (64, 64)  # Patch size for compression artifact detection
RESAMPLE_METHOD = Image.NEAREST  # Resampling method for resizing images
VALID_EXT = ['.bmp', '.dib', '.jpeg', '.jpg', '.jpe', '.jp2', '.png', '.pbm',  # Valid image extensions
             '.pgm', '.ppm', '.sr', '.ras', '.tiff', '.tif']

class ImageFile(File):
    """Class extension from 'File' for image-specific attributes and methods."""

    def __init__(self, basedir, relpath, filename):
        """Add members to supplement File class."""
        File.__init__(self, basedir, relpath, filename)

        self.children['similar'] = []
        self.image = None
        self.small_image = None
        self.thumbnail = None
        self.patch = None
        self.perceptual_hash = None

        return

    def verify_loaded(self):
        """Verify image and derivatives are loaded (only loading when necessary)."""
        if self.image is None:
            try:
                self.image = Image.open(self.abspath)
                self.image.load()  # Necessary b/c of https://github.com/python-pillow/Pillow/issues/1144

                # Compute image derived products
                self.thumbnail = self.image.resize(THUMBNAIL_SIZE)  # Generate thumbnail
                scale_factor = np.min(self.image.size) / float(MAX_DIM_FOR_SMALL)  # Scale down to a small version
                small_size = (np.round(self.image.size[0] / scale_factor).astype('int64'),
                              np.round(self.image.size[1] / scale_factor).astype('int64'))
                left = (small_size[0] - MAX_DIM_FOR_SMALL) // 2
                right = left + MAX_DIM_FOR_SMALL
                upper = (small_size[1] - MAX_DIM_FOR_SMALL) // 2
                lower = upper + MAX_DIM_FOR_SMALL
                self.small_image = self.image.resize(small_size, resample=RESAMPLE_METHOD).crop([left, upper, right, lower])
                #self.small_image = self.image.resize((MAX_DIM_FOR_SMALL, MAX_DIM_FOR_SMALL), resample=RESAMPLE_METHOD)
                self.patch = Image.fromarray(extract_patches_2d(np.array(self.image), PATCH_SIZE, max_patches=1, random_state=0)[0])  # Extract patch
            except OSError:  # Not an image file
                self.image = None

        return

    def compute_perceptual_hash(self, hashfunc=imagehash.average_hash):
        """Calculate perceptual hash (close in value to similar images."""
        self.verify_loaded()
        if self.image is None:  # Couldn't load the image
            return None

        self.perceptual_hash = hashfunc(self.thumbnail)

        return self.perceptual_hash

class ImageFileGroup(FileGroup):
    """Class to operate on an image file group."""
    # Valid extensions for opencv images

    def __init__(self):
        """Initialize new image file group."""
        FileGroup.__init__(self)
        self.THUMBNAIL_SIZE = THUMBNAIL_SIZE
        self.MAX_DIM_FOR_SMALL = MAX_DIM_FOR_SMALL
        self.PATCH_SIZE = PATCH_SIZE
        self.VALID_EXT = VALID_EXT

        return

    # Externally defined methods
    from kaishi.core.image.generator import train_generator
    from kaishi.core.image.generator import generate_validation_data
    from kaishi.core.image.util import get_batch_dimensions
    from kaishi.core.image.filters import filter_similar
    from kaishi.core.image.filters import filter_invalid_file_extensions
    from kaishi.core.image.filters import filter_invalid_image_headers

    def load_dir(self, dir_name):
        """Read file names in a directory while ignoring subdirectories."""
        self.dir_name, self.dir_children, self.files = load_files_by_walk(dir_name, ImageFile)

        return

    def load_instance(self, im_obj):
        """Load a single image instance."""
        im_obj.verify_loaded()

        return

    def load_all(self):
        """Load all with a multiprocessing map."""
        self.pool.map(self.load_instance, self.files)

        return

    def validate_image_header(self, filename):
        """Validate that an image has a valid header.

        Returns True if valid, False if invalid.
        """

        status = imghdr.what(filename)
        if status is not None:
            return True
        else:
            return False

    def build_numpy_batches(self, channels_first=True, batch_size=None, image_type='small_image'):
        """Build a tensor from the entire image corpus (or generate batches if specified).

        If a batch size is specified, this acts as a generator of batches and returns a list of file objects to manipulate.

        'channels_first' - 'True' if channels are the first dimension (standard for PyTorch)
        'image_type' is one of 'thumbnail', 'small_image', or 'patch'
        """
        l = batch_size if batch_size is not None else len(self.files)
        sz = self.get_batch_dimensions(l, channels_first, image_type)
        im_tensor = np.zeros(sz)

        bi = 0
        batch_file_objects = []
        for f in self.files:
            try:
                f.verify_loaded()
                if image_type == 'small_image':
                    im_tensor[bi] = np.array(f.small_image.convert('RGB'))
                elif image_type == 'thumbnail':
                    im_tensor[bi] = np.array(f.thumbnail.convert('RGB'))
                elif image_type == 'patch':
                    im_tensor[bi] = np.array(f.patch.convert('RGB'))
            except AttributeError:
                continue
            bi += 1
            if batch_size is not None:
                batch_file_objects.append(f)
                if bi == batch_size:
                    if channels_first:
                        imtensor = swap_channel_dimension(im_tensor)
                    yield im_tensor, batch_file_objects
                    bi = 0  # Reset the batch

        if batch_size is None:
            if channels_first:
                im_tensor = swap_channel_dimension(im_tensor)

            return im_tensor  # Don't return file objects as it's the same as 'self.files'
