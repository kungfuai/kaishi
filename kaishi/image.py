"""Primary interface to the image tool kit."""
import os
from kaishi.core.image.file import ImageFileGroup


def dataset(source=None):
    """Try to initialize data set object."""
    if source is None:
        dataset_obj = ImageFileGroup()
    elif os.path.isdir(source):
        dataset_obj = ImageFileGroup()
        dataset_obj.load_dir(source)
    # elif os.path.isfile(source):
    #    dataset_obj = ImageFile()

    return dataset_obj

def analyze_dir(dir_name):
    """Analyze and validate a directory of images.

    Returns an image file group object.
    """

    # Load the file names that we will manipulate
    dataset = ImageFileGroup()
    dataset.load_dir(dir_name)

    # Perform filter pipeline
    dataset.filter_by_extension()
    dataset.filter_by_image_header()
    dataset.filter_duplicates()

    # Print report
    dataset.report()

    return dataset
