"""Primary interface to the image tool kit."""
import os
from kaishi.core.file import File
from kaishi.core.file_group import FileGroup


class FileDataset:
    """Factory for generic file dataset objects."""

    def __new__(self, source: str = None, recursive: bool = False):
        """Initialize with the default pipeline defined.

        :param source: string identifying source (e.g. directory)
        :type source: str
        :param recursive: flag to set recursion
        :type recursive: bool
        """
        if os.path.exists(source):
            file_dataset = FileGroup(recursive=recursive)
            file_dataset.load_dir(source, File, file_dataset.recursive)
            return file_dataset
        else:
            raise NotImplementedError("Currently only supports a valid path as input")
