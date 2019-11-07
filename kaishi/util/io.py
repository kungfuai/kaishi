"""Class definition for reading/writing files of various types."""
import os


class FileGroup:
    """Class for reading, writing, and performing general operations of files."""

    def __init__(self):
        """Instantiate empty class."""
        self.file_list = []
        self.invalid_file_list = []

        return

    def from_dir(self, dir_name):
        """Read file names in a directory."""

        self.dir_name = os.path.abspath(dir_name)
        self.file_list = [self.dir_name + '/' + bn for bn in os.listdir(dir_name)]

        return
