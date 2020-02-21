import itertools
import numpy as np
import random
from PIL import Image
from kaishi.core.image.util import swap_channel_dimension
from kaishi.core.image import ops


def augment_and_label(imobj):
    """Augment an image with common issues and return the modified image + label vector.

    LABELS: [DOCUMENT, RECTIFIED, ROTATED_RIGHT, ROTATED_LEFT, UPSIDE_DOWN, STRETCHING]
    """
    label = np.zeros((6,))
    im = imobj.small_image.convert("RGB")

    if "document" in imobj.relative_path:  # Document label
        label[0] = 1

    if np.random.random() < 0.5:  # Remove colors sometimes, no matter the source
        im = im.convert("L").convert("RGB")
    rot_param = np.random.random()  # Rotation (<0.25 does nothing)
    if rot_param <= 0.25:
        label[1] = 1
    elif 0.25 < rot_param <= 0.5:
        im = ops.add_rotation(im, ccw_rotation_degrees=90)
        label[3] = 1
    elif 0.5 < rot_param <= 0.75:
        im = ops.add_rotation(im, ccw_rotation_degrees=180)
        label[4] = 1
    elif rot_param > 0.75:
        im = ops.add_rotation(im, ccw_rotation_degrees=270)
        label[2] = 1
    stretch_param = np.random.random()  # Stretching
    if 0.25 < stretch_param <= 0.75:
        if 0.25 < stretch_param <= 0.5:
            h_stretch = 100
            v_stretch = 0
        elif 0.5 < stretch_param <= 0.75:
            h_stretch = 0
            v_stretch = 100
        pre_stretch_size = im.size
        im = ops.add_stretching(im, h_stretch, v_stretch)
        im = ops.extract_patch(
            im, pre_stretch_size
        )  # Crop back to original size if stretched
        label[5] = 1

    return im, label


def train_generator(self, batch_size=32, string_to_match=None):
    """Generator for training the data labeler. Operates on a kaishi.image.Dataset object.

    'batch_size' - size of batches to create
    'string_to_match' - ignores data without this string in the relative path (make 'None' to use all data)
    """
    indexes = [i for i in range(len(self.files))]
    random.seed(42)
    np.random.seed(42)
    random.shuffle(indexes)

    bi = 0  # Index within batch
    for imind in itertools.cycle(indexes):
        if "validate" in self.files[imind].relative_path:  # Don't use validation data
            continue
        if "high_res" in self.files[imind].relative_path:  # Use only low res photos
            continue
        if (
            string_to_match is not None
            and string_to_match not in self.files[imind].relative_path
        ):
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


def generate_validation_data(self, n_examples=400, string_to_match=None):
    """Generate a reproducibly random validation data set."""
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
        if (
            "validate" not in self.files[imind].relative_path
        ):  # Use only validation data
            continue
        if "high_res" in self.files[imind].relative_path:  # Disregard high res images
            continue
        if (
            string_to_match is not None
            and string_to_match not in self.files[imind].relative_path
        ):
            continue
        self.files[imind].verify_loaded()
        if self.files[imind].image is None:
            continue

        # Perturb the image randomly and label
        X[i], y[i, :] = augment_and_label(self.files[imind])
        i += 1

    X = np.stack(X)

    return swap_channel_dimension(X), y
