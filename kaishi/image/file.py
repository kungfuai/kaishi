"""Definition for image files."""
from PIL import Image
import imagehash
from kaishi.core.file import File
from kaishi.image import ops


THUMBNAIL_SIZE = (64, 64)
MAX_DIM_FOR_SMALL = 224  # Max dimension for small sample
PATCH_SIZE = (64, 64)  # Patch size for compression artifact detection
RESAMPLE_METHOD = Image.NEAREST  # Resampling method for resizing images


class ImageFile(File):
    """Image file object that inherits from the core file class and adds image-specific attributes and methods."""

    def __init__(self, basedir: str, relpath: str, filename: str):
        """Initialize image file object.

        :param basedir: root directory of dataset
        :type basedir: str
        :param relpath: relative directory under the root directory
        :type relpath: str
        :param filename: basename of file
        :type filename: str
        """
        super().__init__(basedir, relpath, filename)
        self.children["similar"] = []
        self.image = None
        self.small_image = None
        self.thumbnail = None
        self.patch = None
        self.perceptual_hash = None

    def verify_loaded(self):
        """Verify image and derivatives are loaded (only performs the load if the image is unloaded)."""
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
        """Update images derived from the base image (i.e. thumbnail, small version, and random patch)."""
        if self.image is not None:
            self.thumbnail = self.image.resize(THUMBNAIL_SIZE)
            self.small_image = ops.make_small(
                self.image, max_dim=MAX_DIM_FOR_SMALL, resample_method=RESAMPLE_METHOD
            )
            self.patch = ops.extract_patch(self.image, PATCH_SIZE)

    def rotate(self, ccw_rotation_degrees: int):
        """Rotate all instances of image by 'ccw_rotation_degrees'.

        :param ccw_rotation_degrees: degrees to rotate the image by
        :type ccw_rotation_degrees: int
        """
        self.image = self.image.rotate(ccw_rotation_degrees, expand=True)
        self.update_derived_images()

    def limit_dimensions(
        self, max_width: int = None, max_height: int = None, max_dimension: int = None
    ):
        """Limit the max dimension of the image and resize accordingly. Any combination of these
        arguments can be defined, however, if none are defined, this method does nothing.

        :param max_width:  maximum width of the image
        :type max_width: int
        :param max_height: maximum height of the image
        :type max_height: int
        :param max_dimension: maximum width or height (applies to both)
        :type max_dimension: int
        """
        if self.image is None:
            return
        if max_dimension is not None:
            max_width = max_dimension
            max_height = max_dimension
        width_factor = 0 if max_width is None else float(self.image.size[0]) / max_width
        height_factor = (
            0 if max_height is None else float(self.image.size[1]) / max_height
        )
        if width_factor <= 1 and height_factor <= 1:
            return  # Image already under limit(s)
        factor = max((width_factor, height_factor))
        self.image = self.image.resize(
            (round(self.image.size[0] / factor), round(self.image.size[1] / factor))
        )
        self.update_derived_images()

    def convert_to_grayscale(self):
        """Convert image to grayscale."""
        if self.image is not None:
            self.image = self.image.convert("L")
            self.add_label("GRAYSCALE")
            self.update_derived_images()
        return self.image

    def compute_perceptual_hash(self, hashfunc=imagehash.average_hash):
        """Calculate perceptual hash (close in value to similar images.

        :param hashfunc: function object to be used to calculate the hash value (defualts to `imagehash.average_hash`)
        :type hashfunc: function
        :return: hash value (as computed by `hashfunc`)
        """
        self.verify_loaded()
        if self.image is None:  # Couldn't load the image
            return None

        self.perceptual_hash = hashfunc(self.thumbnail)

        return self.perceptual_hash
