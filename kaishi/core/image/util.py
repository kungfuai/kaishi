import numpy as np
import imghdr


def swap_channel_dimension(tensor):
    """Swap between channels_first and channels_last.

    If 'tensor' has 4 elements, it's assumed to be the shape vector. Otherwise, it's
    assumed that it's the actual tensor. Returns the edited shape vector or tensor.
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


def validate_image_header(filename):
    """Validate that an image has a valid header.

    Returns True if valid, False if invalid.
    """

    status = imghdr.what(filename)
    if status is not None:
        return True
    else:
        return False


def get_batch_dimensions(
    self, batch_size, channels_first=True, image_type="small_image"
):
    """Get dimensions of the batch tensor. Note that the 'batch_size' argument can be the full data set."""
    if image_type == "small_image":  # Get size of the tensor
        sz = (batch_size, self.MAX_DIM_FOR_SMALL, self.MAX_DIM_FOR_SMALL, 3)
    elif image_type == "thumbnail":
        sz = (batch_size, self.THUMNAIL_SIZE[0], self.THUMBNAIL_SIZE[1], 3)
    elif image_type == "patch":
        sz = (batch_size, self.PATCH_SIZE[0], self.PATCH_SIZE[1], 3)

    if channels_first:
        return swap_channel_dimension(sz)
    else:
        return sz
