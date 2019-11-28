from io import BytesIO
import numpy as np
from PIL import Image


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

    return image.resize(newsize)

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

def _train_generator(self, batch_size=16):
    """Generator for training the data labeler. Operates on a kaishi.image.Dataset object."""
    self.files
