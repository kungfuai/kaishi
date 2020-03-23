"""Class definition for reading/writing files of various types."""
import warnings
from kaishi.core.misc import load_files_by_walk
from kaishi.core.pipeline import Pipeline
from kaishi.core.printing import should_print_row
from prettytable import PrettyTable
import pprint
import numpy as np


class FileGroup:
    """Class for reading and performing general operations on groups of files."""

    # Externally defined classes and methods
    from kaishi.core.misc import CollapseChildren
    from kaishi.core.filters.duplicate_files import FilterDuplicateFiles
    from kaishi.core.filters.by_regex import FilterByRegex
    from kaishi.core.filters.subsample import FilterSubsample
    from kaishi.core.filters.by_label import FilterByLabel
    from kaishi.core.labelers.validation_and_test import LabelerValidationAndTest

    def __init__(self, recursive: bool):
        """Instantiate empty class.

        :param recursive: flag to indicate recursion
        :type recursive: bool
        """
        self.files = []
        self.filtered = dict()
        self.artifacts = dict()
        self.pipeline = Pipeline()
        self.dir_name = None
        self.dir_children = None
        self.files = None
        self.recursive = recursive

    def __getitem__(self, key):
        """Get a specific file object."""
        for fobj in self.files:
            if repr(fobj) == key:
                return fobj
        raise KeyError(key + " not a valid file")

    def load_dir(self, source: str, file_initializer, recursive: bool):
        """Read file names in a directory

        :param source: Directory to load from
        :type source: str
        :param file_initializer: Data file calss to initialize each file with
        :type file_initializer: kaishi file initializer class (e.g. :class:`kaishi.core.file.File`)
        """
        self.dir_name, self.dir_children, self.files = load_files_by_walk(
            source, file_initializer, recursive
        )

    def get_pipeline_options(self):
        """Returns available pipeline options for this dataset.

        :return: list of uninitialized pipeline component objects
        :rtype: list
        """
        options = []
        for method in dir(self):
            if method.startswith("Filter"):
                options.append(method)
        for method in dir(self):
            if method.startswith("Labeler"):
                options.append(method)
        for method in dir(self):
            if method.startswith("Transform"):
                options.append(method)
        for method in dir(self):
            if method.startswith("Aggregator"):
                options.append(method)

        return options

    def configure_pipeline(self, choices: list = None, verbose: bool = False):
        """Configures the sequence of components in the data processing pipeline.

        :param choices: list of pipeline choices
        :type choices: list
        :param verbose: flag to indicate verbosity
        :type verbose: bool
        """
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
                print(repr(i) + ": " + option)
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
            if isinstance(choice, str):
                try:
                    self.pipeline.add_component(self.__getattribute__(choice)())
                except AttributeError:
                    warnings.warn(
                        choice + " is an invalid pipeline component, skipping..."
                    )
            elif isinstance(choice, np.int64):
                self.pipeline.add_component(self.__getattribute__(options[choice])())
            elif callable(choice):
                self.pipeline.add_component(choice)

        if verbose:
            print(repr(self.pipeline))

    def file_report(self, max_file_entries=16, max_filter_entries=10):
        """Show a report of valid and invalid data.

        :param max_file_entries: max number of entries to print of file list
        :type max_file_entries: int
        :param max_filter_entries: max number of entries to print per filter category (e.g. duplicates, similar, etc.)
        :type max_filter_entries: int
        """
        if self.files == [] and self.filtered == {}:
            print("No data loaded to report on.")
            return

        pp = pprint.PrettyPrinter()
        print("Current file list:")
        table = PrettyTable()
        table.field_names = ["Index", "File Name", "Children", "Labels"]
        table.align["Children"] = "l"
        for i, fobj in enumerate(self.files):
            if should_print_row(i, max_file_entries, len(self.files)) == 1:
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
            elif should_print_row(i, max_file_entries, len(self.files)) == 2:
                table.add_row(["...", " ", " ", " "])
        print(table)

        print("Filtered files:")
        table = PrettyTable()
        table.field_names = ["File Name", "Filter Reason"]
        for k in self.filtered:
            for i, fobj in enumerate(self.filtered[k]):
                if should_print_row(i, max_filter_entries, len(self.filtered[k])) == 1:
                    table.add_row([repr(fobj), k])
                elif (
                    should_print_row(i, max_filter_entries, len(self.filtered[k])) == 2
                ):
                    table.add_row(["...", " "])
        print(table)

    def run_pipeline(self, verbose: bool = False):
        """Run the pipeline as configured.

        :param verbose: flag to indicate verbosity
        :type verbose: bool
        """
        self.pipeline(self, verbose=verbose)
        if verbose:
            print("Pipeline completed")
