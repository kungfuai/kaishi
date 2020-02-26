"""Class definition for reading/writing files of various types."""
import os
from kaishi.util.labels import Labels
from kaishi.util.misc import md5sum
from kaishi.util.misc import load_files_by_walk
from kaishi.util.pipeline import Pipeline
import multiprocessing
from prettytable import PrettyTable
import numpy as np


class File:
    """Class that contains details about a file."""

    def __init__(self, basedir, relpath, filename):
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

        return

    def __repr__(self):
        if self.relative_path is None:
            return self.basename
        else:
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

    def __init__(self):
        """Instantiate empty class."""
        self.files = []
        self.filtered = dict()
        self.pipeline = Pipeline()

    # Externally defined classes and methods
    from kaishi.util.misc import CollapseChildren
    from kaishi.util.filters import FilterDuplicates

    def load_dir(self, dir_name):
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

    def configure(self, choice_inds=None):
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

    def report(self):
        """Show a report of valid and invalid data."""
        if self.files == [] and self.filtered == {}:
            print("No data loaded to report on.")
            return

        print("Current file list:")
        x = PrettyTable()
        x.field_names = ["File Name", "Children", "Labels"]
        for f in self.files:
            x.add_row(
                [repr(f), repr(f.children), repr([label.name for label in f.labels])]
            )
        print(x)

        print("Filtered files:")
        x = PrettyTable()
        x.field_names = ["File Name", "Filter Reason"]
        for k in self.filtered:
            for f in self.filtered[k]:
                x.add_row([repr(f), k])
        print(x)
