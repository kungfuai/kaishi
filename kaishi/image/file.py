"""Definitions for image file objects and groups of them."""
import os
from PIL import Image
import imagehash
from kaishi.core.file import File
from kaishi.core.labels import Labels
from kaishi.image import ops


THUMBNAIL_SIZE = (64, 64)
MAX_DIM_FOR_SMALL = 224  # Max dimension for small sample
PATCH_SIZE = (64, 64)  # Patch size for compression artifact detection
RESAMPLE_METHOD = Image.NEAREST  # Resampling method for resizing images


class ImageFile(File):
    """Class extension from 'File' for image-specific attributes and methods."""

    def __init__(self, basedir: str, relpath: str, filename: str):
        """Add members to supplement File class."""
        super().__init__(basedir, relpath, filename)
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
                self.update_derived_images()
                if "L" in self.image.mode:
                    self.add_label("GRAYSCALE")
            except OSError:  # Not an image file
                self.image = None

    def update_derived_images(self):
        """Update images derived from the base image."""
        if self.image is not None:
            self.thumbnail = self.image.resize(THUMBNAIL_SIZE)
            self.small_image = ops.make_small(
                self.image, max_dim=MAX_DIM_FOR_SMALL, resample_method=RESAMPLE_METHOD
            )
            self.patch = ops.extract_patch(self.image, PATCH_SIZE)

    def rotate(self, ccw_rotation_degrees: int):
        """Rotate all instances of image by 'ccw_rotation_degrees'."""
        self.image = self.image.rotate(ccw_rotation_degrees, expand=True)
        self.update_derived_images()

    def convert_to_grayscale(self):
        """Convert image to grayscale."""
        if self.image is not None:
            self.image = self.image.convert("L")
            self.add_label("GRAYSCALE")
            self.update_derived_images()
        return self.image

    def compute_perceptual_hash(self, hashfunc=imagehash.average_hash):
        """Calculate perceptual hash (close in value to similar images."""
        self.verify_loaded()
        if self.image is None:  # Couldn't load the image
            return None

        self.perceptual_hash = hashfunc(self.thumbnail)

        return self.perceptual_hash
