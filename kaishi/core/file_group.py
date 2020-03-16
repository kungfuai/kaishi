"""Class definition for reading/writing files of various types."""
import os
import warnings
from kaishi.core.misc import load_files_by_walk
from kaishi.core.pipeline import Pipeline
from prettytable import PrettyTable
import pprint
import numpy as np


class FileGroup:
    """Class for readind and performing general operations on files."""

    # Externally defined classes and methods
    from kaishi.core.misc import CollapseChildren
    from kaishi.core.filters.duplicate_files import FilterDuplicateFiles
    from kaishi.core.filters.by_regex import FilterByRegex
    from kaishi.core.filters.subsample import FilterSubsample
    from kaishi.core.filters.by_label import FilterByLabel
    from kaishi.core.labelers.validation_and_test import LabelerValidationAndTest

    def __init__(self, recursive: bool):
        """Instantiate empty class."""
        self.files = []
        self.filtered = dict()
        self.pipeline = Pipeline()
        self.dir_name = None
        self.dir_children = None
        self.files = None
        self.recursive = recursive

    def load_dir(self, source: str, file_initializer, recursive: bool):
        """Read file names in a directory while ignoring subdirectories."""
        self.dir_name, self.dir_children, self.files = load_files_by_walk(
            source, file_initializer, recursive
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

    def configure_pipeline(self, choices: list = None, verbose: bool = False):
        """Configures the data processing pipeline."""
        options = self.get_pipeline_options()
        if choices is None:  # Prompt for choices if not provided

            def fix_choice_string(choice_string, options):
                choices = np.array(choice_string.split(",")).astype(np.int64)
                if np.any(choices < 0) or np.max(choices) > len(options) - 1:
                    choices = None
                return choices

            verbose = True
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
                    choices = fix_choice_string(choice_string, options)
                except ValueError:
                    choices = None
                if choices is None:
                    choice_string = input(
                        "Error parsing string, please re-enter a list of the above options: "
                    )
                    choices = fix_choice_string(choice_string, options)
        self.pipeline.reset()
        for choice in choices:  # Use the configuration specified to construct pipeline
            if isinstance(choice, np.int64):
                self.pipeline.add_component(options[choice]())
            elif isinstance(choice, str):
                try:
                    self.pipeline.add_component(self.__getattribute__(choice)())
                except AttributeError:
                    warnings.warn(
                        choice + " is an invalid pipeline component, skipping..."
                    )
            elif callable(choice):
                self.pipeline.add_component(choice)
        
        if verbose:
            print(repr(self.pipeline))

    def should_print_row(self, i, max_entries, num_entries):
        """Make decision to print row or not based on max_rows."""
        if num_entries <= max_entries:
            return 1
        else:
            gap_i_lower = max_entries // 2
            gap_i_upper = num_entries - (max_entries - gap_i_lower)
            if i == gap_i_lower:
                # Ellipsis line
                return 2
            elif i <= gap_i_lower or i >= gap_i_upper:
                # Print data
                return 1
            else:
                # Do not print
                return 0

    def file_report(self, max_file_entries=30, max_filter_entries=10):
        """Show a report of valid and invalid data."""
        if self.files == [] and self.filtered == {}:
            print("No data loaded to report on.")
            return

        pp = pprint.PrettyPrinter()
        print("Current file list:")
        table = PrettyTable()
        table.field_names = ["Index", "File Name", "Children", "Labels"]
        table.align["Children"] = "l"
        for i, fobj in enumerate(self.files):
            if self.should_print_row(i, max_file_entries, len(self.files)) == 1:
                children_text = pp.pformat(fobj.children).split("\n")
                table.add_row(
                    [
                        i,
                        repr(fobj),
                        "    " + children_text[0],
                        repr([label.name for label in fobj.labels]),
                    ]
                )
                if len(children_text) > 1:
                    for child_line in children_text[1:]:
                        table.add_row([" ", " ", "\t" + child_line, " "])
            elif self.should_print_row(i, max_file_entries, len(self.files)) == 2:
                table.add_row(["...", " ", " ", " "])
        print(table)

        print("Filtered files:")
        table = PrettyTable()
        table.field_names = ["File Name", "Filter Reason"]
        for k in self.filtered:
            for i, fobj in enumerate(self.filtered[k]):
                if (
                    self.should_print_row(i, max_filter_entries, len(self.filtered[k]))
                    == 1
                ):
                    table.add_row([repr(fobj), k])
                elif (
                    self.should_print_row(i, max_filter_entries, len(self.filtered[k]))
                    == 2
                ):
                    table.add_row(["...", " "])
        print(table)

    def run_pipeline(self, pool: bool = False, verbose: bool = False):
        """Run the pipeline as configured."""
        self.pipeline(self, verbose=verbose)
        if verbose:
            print("Pipeline completed")
