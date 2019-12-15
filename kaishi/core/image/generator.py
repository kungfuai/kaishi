from io import BytesIO
import itertools
import numpy as np
import random
from PIL import Image
from kaishi.core.image.util import swap_channel_dimension


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

def augment_and_label(imobj):
    """Augment an image with common issues and return the modified image + label vector.

    LABELS: [DOCUMENT, RECTIFIED, ROTATED_RIGHT, ROTATED_LEFT, UPSIDE_DOWN, STRETCHING]
    """
    label = np.zeros((6,))
    im = imobj.small_image.convert('RGB')

    if 'document' in imobj.relative_path:  # Document label
        label[0] = 1

    if np.random.random() < 0.5:  # Remove colors sometimes, no matter the source
        im = im.convert('L').convert('RGB')
    rot_param = np.random.random()  # Rotation (<0.25 does nothing)
    if rot_param <= 0.25:
        label[1] = 1
    elif 0.25 < rot_param <= 0.5:
        im = add_rotation(im, ccw_rotation_degrees=90)
        label[3] = 1
    elif 0.5 < rot_param <= 0.75:
        im = add_rotation(im, ccw_rotation_degrees=180)
        label[4] = 1
    elif rot_param > 0.75:
        im = add_rotation(im, ccw_rotation_degrees=270)
        label[2] = 1
    stretch_param = np.random.random()  # Stretching
    if 0.25 < stretch_param <= 0.75:
        if 0.25 < stretch_param <= 0.5:
            h_stretch = 100
            v_stretch = 0
        elif 0.5 < stretch_param <= 0.75:
            h_stretch = 0
            v_stretch = 100
        im = add_stretching(im, h_stretch, v_stretch)
        sz_baseline = np.min(im.size)  # Crop back to size if it's stretched
        left = (im.size[0] - sz_baseline) // 2
        right = left + sz_baseline
        upper = (im.size[1] - sz_baseline) // 2
        lower = upper + sz_baseline
        im = im.crop([left, upper, right, lower])
        label[5] = 1

    return im, label

def _train_generator(self, batch_size=32, string_to_match=None):
    """Generator for training the data labeler. Operates on a kaishi.image.Dataset object.

    LABELS: [DOCUMENT, RECTIFIED, ROTATED_RIGHT, ROTATED_LEFT, UPSIDE_DOWN, STRETCHING]
    Additional labels to implement with a different network: compressed, noisy

    'batch_size' - size of batches to create
    'string_to_match' - ignores data without this string in the relative path (make 'None' to use all data)
    """
    indexes = [i for i in range(len(self.files))]
    random.seed(42)
    np.random.seed(42)
    random.shuffle(indexes)

    bi = 0  # Index within batch
    for imind in itertools.cycle(indexes):
        if 'validate' in self.files[imind].relative_path:  # Don't use validation data
            continue
        if 'high_res' in self.files[imind].relative_path:  # Use only PASCAL photos
            continue
        if string_to_match is not None and string_to_match not in self.files[imind].relative_path:
            continue
        self.files[imind].verify_loaded()
        if self.files[imind].image is None:
            continue

        if bi == 0:  # Initialize the batch if needed
            batch = [None] * batch_size
            labels = np.zeros((batch_size, 6))

        # Perturb the image randomly and label
        batch[bi], labels[bi, :] = augment_and_label(self.files[imind])

        if bi == batch_size - 1:
            bi = 0
            batch = np.stack(batch)
            yield swap_channel_dimension(batch), labels
        else:
            bi += 1

def _generate_validation_data(self, n_examples=400, string_to_match=None):
    """Generate a reproducibly random validation data set.

    LABELS: [DOCUMENT, RECTIFIED, ROTATED_RIGHT, ROTATED_LEFT, UPSIDE_DOWN, STRETCHING]
    """
    indexes = [i for i in range(len(self.files))]
    random.seed(42)
    np.random.seed(42)
    random.shuffle(indexes)
    X = [None] * n_examples
    y = np.zeros((n_examples, 6))
    i = 0

    for imind in itertools.cycle(indexes):
        if i == n_examples:
            break
        if 'validate' not in self.files[imind].relative_path:  # Use only validation data
            continue
        if 'high_res' in self.files[imind].relative_path:  # Disregard high res images
            continue
        if string_to_match is not None and string_to_match not in self.files[imind].relative_path:
            continue
        self.files[imind].verify_loaded()
        if self.files[imind].image is None:
            continue

        # Perturb the image randomly and label
        X[i], y[i, :] = augment_and_label(self.files[imind])
        i += 1

    X = np.stack(X)
    return swap_channel_dimension(X), y
