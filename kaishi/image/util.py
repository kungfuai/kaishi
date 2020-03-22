"""Image utilities and helper functions."""
import numpy as np
import imghdr


def swap_channel_dimension(tensor):
    """Swap between channels_first and channels_last.

    If 'tensor' has 4 elements, it's assumed to be the shape vector. Otherwise, it's
    assumed that it's the actual tensor. Returns the edited shape vector or tensor.

    :param tensor: shape vector or tensor to have channel dimensions swapped
    :type tensor: `numpy.array`
    :return: altered input with the channel dimensions swapped
    :rtype: `numpy.array`
    """
    if np.size(tensor) == 4:  # Shape vector
        if tensor[-1] == 3 or tensor[-1] == 1:
            return np.array([tensor[0], tensor[3], tensor[1], tensor[2]])
        else:
            return np.array([tensor[0], tensor[2], tensor[3], tensor[1]])
    else:  # Full tensor
        if np.shape(tensor)[-1] == 3 or np.shape(tensor)[-1] == 1:
            return np.swapaxes(np.swapaxes(tensor, 2, 3), 1, 2)
        else:
            return np.swapaxes(np.swapaxes(tensor, 1, 2), 2, 3)


def validate_image_header(filename: str):
    """Validate that an image has a valid header.

    Returns True if valid, False if invalid.

    :param filename: name of file to analyze
    :type filename: str
    :return: flag indicating whether header is valid (by using `imghdr.what()`)
    :rtype: bool
    """

    status = imghdr.what(filename)
    if status is not None:
        return True
    else:
        return False


def get_batch_dimensions(
    self, batch_size: int, channels_first: bool = True, image_type: str = "small_image"
):
    """Get dimensions of the batch tensor. Note that the 'batch_size' argument can be the full data set.

    :param self: image dataset object
    :type self: :class:`kaishi.image.dataset.ImageDataset`
    :param batch_size: batch size
    :type batch_size: int
    :param channels_first: flag indicating whether channels are first or last dimension in each image
    :type channels_first: bool
    :param image_type: one of "small_image", "thumbnail", or "patch"
    :type image_type: str
    :return: batch dimesions (4D tuple)
    :rtype: tuple
    """
    if image_type == "small_image":  # Get size of the tensor
        sz = (batch_size, self.max_dim_for_small, self.max_dim_for_small, 3)
    elif image_type == "thumbnail":
        sz = (batch_size, self.thumbnail_size[0], self.thumbnail_size[1], 3)
    elif image_type == "patch":
        sz = (batch_size, self.patch_size[0], self.patch_size[1], 3)

    if channels_first:
        return swap_channel_dimension(sz)
    else:
        return sz
