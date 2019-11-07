"""Primary interface to the image tool kit."""
from kaishi.core.image.file import ImageFileGroup


def dataset():
    """Blank image dataset object."""
    return ImageFileGroup()

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
