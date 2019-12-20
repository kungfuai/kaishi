import os
import copy
import numpy as np
from PIL import Image
import imagehash
from tqdm import tqdm
from kaishi.util.file import File, FileGroup
from kaishi.util.misc import load_files_by_walk
from kaishi.core.image.util import swap_channel_dimension
from kaishi.core.image.util import normalize_image
from kaishi.core.image.model import Model
from kaishi.core.image import ops
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
                self.thumbnail = self.image.resize(THUMBNAIL_SIZE)
                self.small_image = ops.make_small(self.image, max_dim=MAX_DIM_FOR_SMALL, resample_method=RESAMPLE_METHOD)
                self.patch = ops.extract_patch(self.image, PATCH_SIZE)
            except OSError:  # Not an image file
                self.image = None

        return

    def rotate(self, ccw_rotation_degrees):
        """Rotate all instances of image by 'ccw_rotation_degrees'."""
        self.image = self.image.rotate(ccw_rotation_degrees, expand=True)
        self.thumbnail = self.thumbnail.rotate(ccw_rotation_degrees, expand=True)
        self.small_image = self.small_image.rotate(ccw_rotation_degrees, expand=True)
        self.patch = self.patch.rotate(ccw_rotation_degrees, expand=True)

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
    def __init__(self):
        """Initialize new image file group."""
        FileGroup.__init__(self)
        self.THUMBNAIL_SIZE = THUMBNAIL_SIZE
        self.MAX_DIM_FOR_SMALL = MAX_DIM_FOR_SMALL
        self.PATCH_SIZE = PATCH_SIZE
        self.VALID_EXT = VALID_EXT
        self.model = None  # Only load model if needed
        self.labeled = False

        return

    # Externally defined methods
    from kaishi.core.image.generator import train_generator
    from kaishi.core.image.generator import generate_validation_data
    from kaishi.core.image.util import get_batch_dimensions
    from kaishi.core.image.filters import filter_similar
    from kaishi.core.image.filters import filter_invalid_file_extensions
    from kaishi.core.image.filters import filter_invalid_image_headers
    from kaishi.core.image.transforms import transform_fix_rotation

    def load_dir(self, dir_name):
        """Read file names in a directory while ignoring subdirectories."""
        self.dir_name, self.dir_children, self.files = load_files_by_walk(dir_name, ImageFile)

        return

    def load_all(self):
        """Load all files."""
        for f in self.files:
            f.verify_loaded()

        return

    def build_numpy_batches(self, channels_first=True, batch_size=None, image_type='small_image'):
        """Build a tensor from the entire image corpus (or generate batches if specified).

        If a batch size is specified, this acts as a generator of batches and returns a list of file objects to manipulate.

        'channels_first' - 'True' if channels are the first dimension (standard for PyTorch)
        'image_type' is one of 'thumbnail', 'small_image', or 'patch'
        """
        l = batch_size if batch_size is not None else len(self.files)
        sz = self.get_batch_dimensions(l, channels_first=False, image_type=image_type)  # Start with PIL-style channel layout
        im_tensor = np.zeros(sz)

        bi = 0
        batch_file_objects = []
        for f in self.files:
            try:
                f.verify_loaded()
                if image_type == 'small_image':
                    im_tensor[bi] = np.array(normalize_image(f.small_image.convert('RGB')))
                elif image_type == 'thumbnail':
                    im_tensor[bi] = np.array(normalize_image(f.thumbnail.convert('RGB')))
                elif image_type == 'patch':
                    im_tensor[bi] = np.array(normalize_image(f.patch.convert('RGB')))
            except AttributeError:
                continue
            bi += 1
            if batch_size is not None:
                batch_file_objects.append(f)
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
            else:
                return im_tensor  # Don't return file objects as it's the same as 'self.files'
        elif batch_size is not None and len(batch_file_objects) > 0:
            if channels_first:
                yield swap_channel_dimension(im_tensor), batch_file_objects
            else:
                yield im_tensor, batch_file_objects

    def predict_and_label(self):
        """Use pre-trained ConvNet to predict image labels (e.g. stretched, rotated, etc.)."""
        if self.model is None:
            self.model = Model()
        for batch, fobjs in self.build_numpy_batches(batch_size=self.model.batch_size):
            pred = self.model.predict(batch)
            for i in range(len(fobjs)):
                if pred[i, 0] > 0.5:
                    fobjs[i].add_label('DOCUMENT')
                rot = np.argmax(pred[i, 1:5])
                if rot == 0:
                    fobjs[i].add_label('RECTIFIED')
                elif rot == 1:
                    fobjs[i].add_label('ROTATED_RIGHT')
                elif rot == 2:
                    fobjs[i].add_label('ROTATED_LEFT')
                else:
                    fobjs[i].add_label('UPSIDE_DOWN')
                if pred[i, 5] > 0.5:
                    fobjs[i].add_label('STRETCHED')
        self.labeled = True

        return

    def save(self, out_dir):
        """Save image data set in the same structure as the original data set, save for the filtered elements."""
        out_dir = os.path.abspath(out_dir)
        if not os.path.exists(out_dir):  # Ensure output directory exists
            os.makedirs(out_dir)
        for f in self.files:  # Determine file paths and save
            if f.image is None:
                continue
            if f.relative_path is not None:
                file_dir = os.path.join(out_dir, f.relative_path)
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
            else:
                file_dir = out_dir
            f.image.save(os.path.join(file_dir, f.basename))

        return
