"""Definitions for image file objects and groups of them."""
import os
import pandas as pd
from kaishi.core.file_group import FileGroup
from kaishi.core.misc import load_files_by_walk
from kaishi.tabular.file import TabularFile


class TabularFileGroup(FileGroup):
    """Class to operate on an image file group."""

    # Externally defined classes and methods
    from kaishi.tabular.filters.duplicate_rows_each_dataframe import (
        FilterDuplicateRowsEachDataframe,
    )
    from kaishi.tabular.filters.duplicate_rows_after_concatenation import (
        FilterDuplicateRowsAfterConcatenation,
    )
    from kaishi.tabular.filters.invalid_file_extensions import (
        FilterInvalidFileExtensions,
    )

    def __init__(self, recursive: bool):
        """Initialize new image file group."""
        super().__init__(recursive)
        self.df_concatenated = None

    def get_valid_dataframes(self):
        """Get a list of valid dataframes."""
        valid_dataframes = []
        for fobj in self.files:
            fobj.verify_loaded()
            if fobj.df is not None:
                valid_dataframes.append(fobj.df)

        return valid_dataframes

    def concatenate_all(self):
        """Concatenate all tables."""
        if self.df_concatenated is None:
            self.df_concatenated = pd.concat(self.get_valid_dataframes()).reset_index(
                drop=True
            )

    def load_dir(self, dir_name: str):
        """Read file names in a directory while ignoring subdirectories."""
        self.dir_name, self.dir_children, self.files = load_files_by_walk(
            dir_name, TabularFile, recursive=self.recursive
        )

    def save(self, out_dir: str, file_format: str = "csv"):
        """Save the dataset as-is."""
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        if self.df_concatenated is not None:
            if file_format == "csv":
                self.df_concatenated.to_csv(
                    os.path.join(out_dir, "all.csv"), index=False
                )
            else:
                raise NotImplementedError
        else:
            for fobj in self.files:  # Determine file paths and save
                fobj.verify_loaded()
                if fobj.load_error:
                    continue
                if fobj.relative_path is not None:
                    file_dir = os.path.join(out_dir, fobj.relative_path)
                    if not os.path.exists(file_dir):
                        os.makedirs(file_dir)
                else:
                    file_dir = out_dir
                if file_format == "csv":
                    fobj.df.to_csv(os.path.join(file_dir, fobj.basename))
                else:
                    raise NotImplementedError
