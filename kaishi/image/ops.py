"""Definitions for common operations on images."""
from io import BytesIO
import numpy as np
from PIL import Image


def extract_patch(im, patch_size):
    """Extract a center cropped patch of size 'patch_size' (2-element tuple).

    :param im: input image
    :type im: PIL image object
    :param patch_size: size of patch
    :type patch_size: tuple, array, or similar
    :return: center-cropped patch
    :rtype: PIL image object
    """
    left = (im.size[0] - patch_size[0]) // 2
    top = (im.size[1] - patch_size[1]) / 2
    right = left + patch_size[0]
    bottom = top + patch_size[1]

    return im.crop([left, top, right, bottom])


def make_small(im, max_dim: int = 224, resample_method=Image.NEAREST):
    """Make a small version of an image while maintaining aspect ratio.

    :param im: input image
    :type im: PIL image object
    :param max_dim: maximum dimension of resized image (x or y)
    :type max_dim: int
    :param resample_method: method for resampling the image
    :type resample_method: PIL resample method
    :return: resized image
    :rtype: PIL image object
    """
    scale_factor = np.min(im.size) / float(max_dim)  # Scale down to a small version
    small_size = (
        np.round(im.size[0] / scale_factor).astype("int64"),
        np.round(im.size[1] / scale_factor).astype("int64"),
    )
    left = (small_size[0] - max_dim) // 2
    right = left + max_dim
    upper = (small_size[1] - max_dim) // 2
    lower = upper + max_dim

    return im.resize(small_size, resample=resample_method).crop(
        [left, upper, right, lower]
    )


def add_jpeg_compression(im, quality_level: int = 30):
    """Apply JPEG compression to an image with a given quality level.

    :param im: input image
    :type im: PIL image object
    :param quality_level: JPEG qualit level, where: 0 < value <= 100
    :type quality_level: int
    :return: compressed image
    :rtype: PIL image object
    """
    buf = BytesIO()
    im.save(buf, "JPEG", q=int(quality_level))

    return Image.open(buf)


def add_rotation(im, ccw_rotation_degrees: int = 90):
    """Rotate an image CCW by `ccw_rotation_degrees` degrees.

    :param im: input image
    :type im: PIL image object
    :param ccw_rotation_degrees: number of degrees to rotate counter-clockwise
    :type ccw_rotation_degrees: int
    :return: rotated image
    :rtype: PIL image object
    """
    return im.rotate(ccw_rotation_degrees, expand=True)


def add_stretching(im, w_percent_additional, h_percent_additional):
    """Stretch an image by the specified percentages.

    :param im: input image
    :type im: PIL image object
    :param w_percent_additional: amount of width stretching to add (0 maintains the same size, 100 doubles the size)
    :type w_percent_additional: int or float greater than 0
    :param h_percent_additional: amount of height stretching to add (0 maintains the same size, 100 doubles the size)
    :type h_percent_additional: int or float greater than 0
    :return: stretched image
    :rtype: PIL image object
    """
    newsize = (
        im.size[0] * int(1.0 + float(w_percent_additional) / 100),
        im.size[1] * int(1.0 + float(h_percent_additional) / 100),
    )

    return im.resize(newsize, resample=Image.BILINEAR)


def add_poisson_noise(im, param: float = 1.0, rescale: bool = True):
    """Add Poisson noise to image, where (poisson noise * `param`) is the final noise function.

    See http://kmdouglass.github.io/posts/modeling-noise-for-image-simulations for more info.
    If `rescale` is set to True, the image will be rescaled after noise is added. Otherwise,
    the noise will saturate.

    :param im: input image
    :type im: PIL image object
    :param param: noise parameter
    :type param: float
    :param rescale: flag indicating whether or not to rescale the image after adding noise (maintaining original image extrema)
    :type rescale: bool
    :return: image with Poisson noise added
    :rtype: PIL image object
    """
    image_with_standard_noise = np.random.poisson(im)
    noisy_image = np.array(im) + param * image_with_standard_noise

    # Fix values beyond the saturation value or rescale
    saturation_value = im.getextrema()[0][1]
    if rescale:
        noisy_image = noisy_image * (saturation_value / np.max(noisy_image))
    else:
        noisy_image[noisy_image > saturation_value] = saturation_value

    return Image.fromarray(noisy_image.astype(np.uint8))
