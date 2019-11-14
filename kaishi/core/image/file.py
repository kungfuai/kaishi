import os
import imghdr
from PIL import Image
import imagehash
from kaishi.util.file import File, FileGroup
from kaishi.util.misc import trim_list_by_inds
from kaishi.util.misc import find_near_duplicates_by_value
from kaishi.util.misc import load_files_by_walk


class ImageFile(File):
    """Class extension from 'File' for image-specific attributes and methods."""
    THUMBNAIL_SIZE = (64, 64)

    def __init__(self, basedir, relpath, filename):
        """Add members to supplement File class."""
        File.__init__(self, basedir, relpath, filename)

        self.image = None
        self.thumbnail = None
        self.perceptual_hash = None

        return

    def verify_loaded(self):
        """Verify image is loaded, and try to load."""
        if self.image is None:
            try:
                self.image = Image.open(self.abspath)
                self.thumbnail = self.image.resize(self.THUMBNAIL_SIZE)
            except OSError:  # Not an image file:
                self.image = None

        return

    def compute_perceptual_hash(self):
        """Calculate perceptual hash (close in value to similar images."""
        self.verify_loaded()
        if self.image is None:  # Couldn't load the image
            return None

        self.perceptual_hash = imagehash.average_hash(self.thumbnail)

        return self.perceptual_hash

class ImageFileGroup(FileGroup):
    """Class to operate on an image file group."""
    # Valid extensions for opencv images
    VALID_EXT = ['.bmp', '.dib', '.jpeg', '.jpg', '.jpe', '.jp2', '.png', '.pbm',
                 '.pgm', '.ppm', '.sr', '.ras', '.tiff', '.tif']

    def load_dir(self, dir_name):
        """Read file names in a directory while ignoring subdirectories."""
        self.dir_name, self.dir_children, self.files = load_files_by_walk(dir_name, ImageFile)

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

    def filter_near_duplicates(self, threshold):
        """Filter near duplicate files, detected via perceptual hashing ('imagehash' library)."""
        hashlist = [f.perceptual_hash if f.perceptual_hash is not None else f.compute_perceptual_hash() for f in self.files]

        duplicate_ind = find_near_duplicates_by_value(hashlist, threshold)
        self.files, trimmed = trim_list_by_inds(self.files, duplicate_ind)
        self.filtered['near_duplicates'] = trimmed

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
