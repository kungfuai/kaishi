"""Class definition for reading/writing files of various types."""
import os
from kaishi.core.misc import md5sum


class File:
    """Class that contains details about a file."""

    def __init__(self, basedir: str, relpath: str, filename: str):
        """Initialize basic file details."""
        self.relative_path = relpath
        self.children = {"duplicates": []}
        self.labels = []
        _, self.ext = os.path.splitext(filename)
        self.basename = filename
        if relpath is not None:
            self.abspath = os.path.join(basedir, relpath, filename)
        else:
            self.abspath = os.path.join(basedir, filename)
        self.hash = None  # Default to None, populate later

    def __repr__(self):
        if self.relative_path is None:
            return self.basename
        return os.path.join(self.relative_path, self.basename)

    def __str__(self):
        return self.__repr__()

    def compute_hash(self):
        """Compute the hash of the file."""
        self.hash = md5sum(self.abspath)

        return self.hash

    def add_label(self, label):
        """Add a label to a file object."""
        if label not in self.labels:
            self.labels.append(label)

        # Ensure the list is always sorted
        string_list = [label.name for label in self.labels]
        sort_ind = sorted(range(len(string_list)), key=lambda k: string_list[k])
        self.labels = [self.labels[i] for i in sort_ind]

    def remove_label(self, label):
        """Remove a label from a file object."""
        try:
            self.labels.remove(label)
        except ValueError:
            return
