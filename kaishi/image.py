"""Primary interface to the image tool kit."""
from kaishi.core.image.file import ImageFileGroup


def analyze(dir_name):
    # Load the file names that we will manipulate
    images = ImageFileGroup()
    images.from_dir(dir_name)
    print('Files now:')
    print(images.file_list)
    images.filter_by_extension()
    print('Files now:')
    print(images.file_list)
    images.filter_by_image_header()
    print('Files now:')
    print(images.file_list)

    return
