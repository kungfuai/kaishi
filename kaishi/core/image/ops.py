from io import BytesIO
import numpy as np
from PIL import Image


def extract_patch(im, patch_size):
    """Extract a center cropped patch of size 'patch_size' (2-element tuple)."""
    left = (im.size[0] - patch_size[0]) // 2
    top = (im.size[1] - patch_size[1])/2
    right = left + patch_size[0]
    bottom = top + patch_size[1]

    return im.crop([left, top, right, bottom])

def make_small(im, max_dim=224, resample_method=Image.NEAREST):
    """Make a small version of an image while maintaining aspect ratio.

    'im' - input image (PIL format)
    'max_dim' - maximum dimension
    """
    scale_factor = np.min(im.size) / float(max_dim)  # Scale down to a small version
    small_size = (np.round(im.size[0] / scale_factor).astype('int64'),
                  np.round(im.size[1] / scale_factor).astype('int64'))
    left = (small_size[0] - max_dim) // 2
    right = left + max_dim
    upper = (small_size[1] - max_dim) // 2
    lower = upper + max_dim

    return im.resize(small_size, resample=resample_method).crop([left, upper, right, lower])

def add_jpeg_compression(image, quality_level=30):
    """Apply random (unless specified) JPEG compression to an image.

    Quality level is a number < 100."""
    buf = BytesIO()
    image.save(buf, 'JPEG', q=int(quality_level))

    return Image.open(buf)

def add_rotation(image, ccw_rotation_degrees=90):
    """Rotate an image CCW but 'ccw_rotation_degrees' degrees."""
    return image.rotate(ccw_rotation_degrees, expand=True)

def add_stretching(image, w_percent_additional, h_percent_additional):
    """Stretch an image by the specified percentages."""
    newsize = (image.size[0] * int(1.0 + w_percent_additional / 100),
               image.size[1] * int(1.0 + h_percent_additional / 100))

    return image.resize(newsize, resample=Image.BILINEAR)

def add_poisson_noise(image, param=1.0, rescale=True):
    """Add Poisson noise to image, where (poisson noise * param) is the final noise function.

    See http://kmdouglass.github.io/posts/modeling-noise-for-image-simulations for more info.
    If 'rescale' is set to True, the image will be rescaled after noise is added. Otherwise,
    the noise will saturate.
    """
    image_with_standard_noise = np.random.poisson(image)
    noise = image_with_standard_noise - np.array(image)
    noisy_image = np.array(image) + param * image_with_standard_noise

    # Fix values beyond the saturation value or rescale
    saturation_value = image.getextrema()[0][1]
    if rescale:
        noisy_image = noisy_image * (saturation_value / np.max(noisy_image))
    else:
        noisy_image[noisy_image > saturation_value] = saturation_value

    return Image.fromarray(noisy_image.astype(np.uint8))
