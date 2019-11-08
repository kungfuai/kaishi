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

    def filter_by_file_extension(self, valid_ext_list=VALID_EXT):
        """Filter file list if non-image extensions exist."""

        # Trim any files without image extensions 
        badind = []
        for i, f in enumerate(self.files):
            _, ext = os.path.splitext(f.basename)
            if len(ext) == 0 or ext not in valid_ext_list:
                badind.append(i)

        self.files, trimmed = trim_list_by_inds(self.files, badind) 
        self.filtered['unsupported_extension'] = trimmed

        return trimmed

    def filter_invalid_image_headers(self):
        """Filter file list if image files have invalid or nonexistent header."""

        badind = []
        for i, f in enumerate(self.files):
            if not self.validate_image_header(f.abspath):
                badind.append(i)

        self.files, trimmed = trim_list_by_inds(self.files, badind)
        self.filtered['invalid_header'] = trimmed

        return trimmed
