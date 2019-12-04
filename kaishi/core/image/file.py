import os
import copy
import numpy as np
import imghdr
from PIL import Image
import imagehash
from tqdm import tqdm
from kaishi.util.file import File, FileGroup
from kaishi.util.misc import trim_list_by_inds
from kaishi.util.misc import find_similar_by_value
from kaishi.util.misc import load_files_by_walk
from sklearn.feature_extraction.image import extract_patches_2d


class ImageFile(File):
    """Class extension from 'File' for image-specific attributes and methods."""
    THUMBNAIL_SIZE = (64, 64)
    MAX_DIM_FOR_SMALL = 224  # Max dimension for small sample
    PATCH_SIZE = (64, 64)  # Patch size for compression artifact detection
    RESAMPLE_METHOD = Image.NEAREST  # Resampling method for resizing images

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
                self.thumbnail = self.image.resize(self.THUMBNAIL_SIZE)  # Generate thumbnail
                scale_factor = np.min(self.image.size) / float(self.MAX_DIM_FOR_SMALL)  # Scale down to a small version
                small_size = (np.round(self.image.size[0] / scale_factor).astype('int64'),
                              np.round(self.image.size[1] / scale_factor).astype('int64'))
                left = (small_size[0] - self.MAX_DIM_FOR_SMALL) // 2
                right = left + self.MAX_DIM_FOR_SMALL
                upper = (small_size[1] - self.MAX_DIM_FOR_SMALL) // 2
                lower = upper + self.MAX_DIM_FOR_SMALL
                self.small_image = self.image.resize(small_size, resample=self.RESAMPLE_METHOD).crop([left, upper, right, lower])
                self.patch = Image.fromarray(extract_patches_2d(np.array(self.image), self.PATCH_SIZE, max_patches=1, random_state=0)[0])  # Extract patch
            except OSError:  # Not an image file
                self.image = None

        return

    def compute_perceptual_hash(self, hashfunc=imagehash.average_hash):
        """Calculate perceptual hash (close in value to similar images."""
        self.verify_loaded(thumbnail=True)
        if self.image is None:  # Couldn't load the image
            return None

        self.perceptual_hash = hashfunc(self.thumbnail)

        return self.perceptual_hash

class ImageFileGroup(FileGroup):
    """Class to operate on an image file group."""
    # Valid extensions for opencv images
    VALID_EXT = ['.bmp', '.dib', '.jpeg', '.jpg', '.jpe', '.jp2', '.png', '.pbm',
                 '.pgm', '.ppm', '.sr', '.ras', '.tiff', '.tif']

    def __init__(self):
        """Initialize new image file group."""
        FileGroup.__init__(self)

        return

    # Externally defined methods
    from kaishi.core.image.generator import train_generator
    from kaishi.core.image.generator import generate_validation_data

    def load_dir(self, dir_name):
        """Read file names in a directory while ignoring subdirectories."""
        self.dir_name, self.dir_children, self.files = load_files_by_walk(dir_name, ImageFile)

        return

    def load_all(self):
        """Load all images and specific image derivatives."""
        for f in tqdm(self.files):
            f.verify_loaded()

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

    def filter_similar(self, threshold):
        """Filter near duplicate files, detected via perceptual hashing ('imagehash' library)."""
        hashlist = [f.perceptual_hash if f.perceptual_hash is not None else f.compute_perceptual_hash() for f in self.files]

        duplicate_ind, parent_ind = find_similar_by_value(hashlist, threshold)
        for di, pi in zip(duplicate_ind, parent_ind):
            self.files[pi].children['similar'].append(self.files[di])
        self.files, trimmed = trim_list_by_inds(self.files, duplicate_ind)
        self.filtered['similar'] = trimmed

        return trimmed

    def filter_invalid_file_extensions(self, valid_ext_list=VALID_EXT):
        """Filter file list if non-image extensions exist."""

        # Trim any files without image extensions 
        badind = []
        for i, f in enumerate(self.files):
            _, ext = os.path.splitext(f.basename)
            if len(ext) == 0 or ext not in valid_ext_list:
                badind.append(i)

        self.files, trimmed = trim_list_by_inds(self.files, badind) 
        self.filtered['unsupported_extension'] = trimmed

        return trimmed

    def filter_invalid_image_headers(self):
        """Filter file list if image files have invalid or nonexistent header."""

        badind = []
        for i, f in enumerate(self.files):
            if not self.validate_image_header(f.abspath):
                badind.append(i)

        self.files, trimmed = trim_list_by_inds(self.files, badind)
        self.filtered['invalid_header'] = trimmed

        return trimmed
