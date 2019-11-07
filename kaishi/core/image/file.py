import os
import imghdr
from kaishi.util.io import FileGroup
from kaishi.util.misc import trim_list_by_inds

class ImageFileGroup(FileGroup):
    """Class to operate on an image file group."""
    # Valid extensions for opencv images
    VALID_EXT = ['.bmp', '.dib', '.jpeg', '.jpg', '.jpe', '.jp2', '.png', '.pbm',
                 '.pgm', '.ppm', '.sr', '.ras', '.tiff', '.tif']

    def validate_header(self, filename):
        """Validate that an image has a valid header.
        
        Returns True if valid, False if invalid.
        """
        
        try:
            status = imghdr.what(filename)
            if status is not None:
                return True
            else:
                return False
        except IsADirectoryError:
            return False

    def filter_by_extension(self):
        """Filter file list if non-image extensions exist."""

        # Trim any files without image extensions 
        badind = []
        for i, fn in enumerate(self.file_list):
            _, ext = os.path.splitext(fn)
            if len(ext) == 0 or ext not in self.VALID_EXT:
                badind.append(i)
                self.invalid_file_list.append(fn)
        print('Extension filter: filtered %d files out of %d' % (len(badind), len(self.file_list)))

        self.file_list = trim_list_by_inds(self.file_list, badind) 

        return

    def filter_by_image_header(self):
        """Filter file list if image files have invalid or nonexistent header."""

        badind = []
        for i, fn in enumerate(self.file_list):
            if not self.validate_header(fn):
                badind.append(i)
        print('Image header filter: filtered %d files out of %d' % (len(badind), len(self.file_list)))

        self.file_list = trim_list_by_inds(self.file_list, badind)

        return

    def filter_by_convnet(self):
        """Filter with a pre-trained convnet."""

        return
