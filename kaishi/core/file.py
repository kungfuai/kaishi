"""Class definition for reading/writing files of various types."""
import os
from kaishi.core.misc import md5sum
from kaishi.core.misc import load_files_by_walk
from kaishi.core.pipeline import Pipeline
from prettytable import PrettyTable
import numpy as np


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


class FileGroup:
    """Class for readind and performing general operations on files."""

    # Externally defined classes and methods
    from kaishi.core.misc import CollapseChildren
    from kaishi.core.filters import FilterDuplicateFiles

    def __init__(self, recursive: bool):
        """Instantiate empty class."""
        self.files = []
        self.filtered = dict()
        self.pipeline = Pipeline()
        self.dir_name = None
        self.dir_children = None
        self.files = None
        self.recursive = recursive

    def load_dir(self, dir_name: str):
        """Read file names in a directory while ignoring subdirectories."""
        self.dir_name, self.dir_children, self.files = load_files_by_walk(
            dir_name, File
        )

    def pipeline_options(self):
        """Returns available pipeline options."""
        options = []
        for method in dir(self):
            if method.startswith("Filter"):
                options.append(getattr(self, method))
        for method in dir(self):
            if method.startswith("Labeler"):
                options.append(getattr(self, method))
        for method in dir(self):
            if method.startswith("Transform"):
                options.append(getattr(self, method))

        return options

    def configure(self, choice_inds: list = None):
        """Configures the data processing pipeline."""
        options = self.pipeline_options()
        if choice_inds is None:  # Prompt for choices if not provided
            print("Pipeline options: ")
            for i, option in enumerate(options):
                print(repr(i) + ": " + option.__name__)
            print("")

            choice_string = input(
                "To configure, enter a comma separated list of integers: "
            )
            choice_inds = None
            while choice_inds is None:  # Keep trying until a valid string is entered
                try:
                    choice_inds = np.array(choice_string.split(",")).astype("int")
                    if (
                        np.any(choice_inds < 0)
                        or np.max(choice_inds) > len(options) - 1
                    ):
                        choice_inds = None
                except ValueError:
                    choice_inds = None
                if choice_inds is None:
                    choice_string = input(
                        "Error parsing string, please re-enter a list of the above options: "
                    )
        self.pipeline.reset()
        for (
            choice_ind
        ) in choice_inds:  # Use the configuration specified to construct pipeline
            self.pipeline.add_component(options[choice_ind](self))
        self.pipeline.add_component(
            self.CollapseChildren(self)
        )  # Always must end with this component

    def file_report(self):
        """Show a report of valid and invalid data."""
        if self.files == [] and self.filtered == {}:
            print("No data loaded to report on.")
            return

        print("Current file list:")
        table = PrettyTable()
        table.field_names = ["File Name", "Children", "Labels"]
        for fobj in self.files:
            table.add_row(
                [
                    repr(fobj),
                    repr(fobj.children),
                    repr([label.name for label in fobj.labels]),
                ]
            )
        print(table)

        print("Filtered files:")
        table = PrettyTable()
        table.field_names = ["File Name", "Filter Reason"]
        for k in self.filtered:
            for fobj in self.filtered[k]:
                table.add_row([repr(fobj), k])
        print(table)
