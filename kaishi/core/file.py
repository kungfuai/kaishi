"""Class definition for reading/writing files of various types."""
import os
from kaishi.core.labels import Labels
from kaishi.core.misc import is_valid_label
from kaishi.core.misc import md5sum
import warnings


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

    def has_label(self, label_to_check: str):
        """Check if file has a specific label."""
        if not is_valid_label(label_to_check, Labels):
            warnings.warn(
                "Check for label "
                + label_to_check
                + " returns False because label is not valid"
            )
            return False
        return bool(label_to_check in [label.name for label in self.labels])

    def add_label(self, label_to_add: str):
        """Add a label to a file object."""
        if not is_valid_label(label_to_add, Labels):
            raise ValueError(
                "Cannot add label " + str(label_to_add) + " as it is not valid"
            )
        if label_to_add not in self.labels:
            self.labels.append(Labels[label_to_add])

        # Ensure the list is always sorted
        string_list = [label.name for label in self.labels]
        sort_ind = sorted(range(len(string_list)), key=lambda k: string_list[k])
        self.labels = [self.labels[i] for i in sort_ind]

    def remove_label(self, label_to_remove: str):
        """Remove a label from a file object."""
        if not is_valid_label(label_to_remove, Labels):
            warnings.warn(
                "Can't remove " + label_to_remove + " as it is not a valid label"
            )
            return
        try:
            self.labels.remove(Labels[label_to_remove])
        except ValueError:
            return
