"""Class definition for reading/writing files of various types."""
import os
import warnings
from kaishi.core.misc import load_files_by_walk
from kaishi.core.pipeline import Pipeline
from prettytable import PrettyTable
import numpy as np


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

    def get_pipeline_options(self):
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

    def configure_pipeline(self, choices: list = None):
        """Configures the data processing pipeline."""
        options = self.get_pipeline_options()
        if choices is None:  # Prompt for choices if not provided
            print("Pipeline options: ")
            for i, option in enumerate(options):
                print(repr(i) + ": " + option.__name__)
            print("")

            choice_string = input(
                "To configure, enter a comma separated list of integers: "
            )
            choices = None
            while choices is None:  # Keep trying until a valid string is entered
                try:
                    choices = np.array(choice_string.split(",")).astype(np.int64)
                    if np.any(choices < 0) or np.max(choices) > len(options) - 1:
                        choices = None
                except ValueError:
                    choices = None
                if choices is None:
                    choices = input(
                        "Error parsing string, please re-enter a list of the above options: "
                    )
        self.pipeline.reset()
        for choice in choices:  # Use the configuration specified to construct pipeline
            if isinstance(choice, np.int64):
                self.pipeline.add_component(options[choice](self))
            elif isinstance(choice, str):
                try:
                    self.pipeline.add_component(self.__getattribute__(choice)(self))
                except AttributeError:
                    warnings.warn(
                        choice + " is an invalid pipeline component, skipping..."
                    )
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
        table.field_names = ["Index", "File Name", "Children", "Labels"]
        for i, fobj in enumerate(self.files):
            table.add_row(
                [
                    i,
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
