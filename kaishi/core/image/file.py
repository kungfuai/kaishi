import os
import imghdr
from kaishi.util.file import FileGroup
from kaishi.util.misc import trim_list_by_inds

class ImageFileGroup(FileGroup):
    """Class to operate on an image file group."""
    # Valid extensions for opencv images
    VALID_EXT = ['.bmp', '.dib', '.jpeg', '.jpg', '.jpe', '.jp2', '.png', '.pbm',
                 '.pgm', '.ppm', '.sr', '.ras', '.tiff', '.tif']

    def validate_image_header(self, filename):
        """Validate that an image has a valid header.
        
        Returns True if valid, False if invalid.
        """
        
        status = imghdr.what(filename)
        if status is not None:
            return True
        else:
            return False

    def filter_by_extension(self):
        """Filter file list if non-image extensions exist."""

        # Trim any files without image extensions 
        badind = []
        for i, fn in enumerate(self.files):
            _, ext = os.path.splitext(fn)
            if len(ext) == 0 or ext not in self.VALID_EXT:
                badind.append(i)

        self.files, trimmed = trim_list_by_inds(self.files, badind) 
        self.filtered['unsupported_extension'] = trimmed

        return

    def filter_by_image_header(self):
        """Filter file list if image files have invalid or nonexistent header."""

        badind = []
        for i, fn in enumerate(self.files):
            if not self.validate_image_header(fn):
                badind.append(i)

        self.files, trimmed = trim_list_by_inds(self.files, badind)
        self.filtered['invalid_header'] = trimmed

        return
