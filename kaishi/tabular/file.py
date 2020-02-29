"""Definitions for image file objects and groups of them."""
import os
import warnings
import pandas as pd
from kaishi.core.file import File, FileGroup
from kaishi.core.misc import load_files_by_walk


VALID_EXT = [
    ".json",
    ".jsonl",
    ".json.gz",
    ".jsonl.gz",
    ".csv",
    ".csv.gz",
]


class TabularFile(File):
    """Class extension from 'File' for tabular data-specific attributes and methods."""

    def __init__(self, basedir: str, relpath: str, filename: str):
        """Add members to supplement File class."""
        super().__init__(basedir, relpath, filename)
        self.summary = None
        self.df = None
        self.load_error = False

    def _has_csv_file_ext(self):
        """Check if file is variant of .csv"""
        fstr = self.basename.lower()
        return fstr.endswith(".csv.gz") or fstr.endswith(".csv")

    def _has_json_file_ext(self):
        """Check if file is variant of .json"""
        fstr = self.basename.lower()
        return (
            fstr.endswith(".json")
            or fstr.endswith(".jsonl")
            or fstr.endswith(".json.gz")
            or fstr.endswith(".jsonl.gz")
        )

    def verify_loaded(self):
        """Load the file if supported."""
        if self.df is not None:
            return
        if self._has_csv_file_ext():
            self.df = pd.read_csv(self.abspath)
        elif self._has_json_file_ext():
            self.df = pd.read_json(self.abspath)
        else:
            warnings.warn(
                "File "
                + self.abspath
                + " not supported, currently only support .csv or .json formats. Skipping."
            )
            self.load_error = True

    def load_summary(self):
        """Load summary for this data frame."""
        if self.df is None and self.load_error is False:
            self.verify_loaded()  # Try loading if it's None
        if self.load_error:
            return
        if self.summary is None:
            describe = dict()
            fraction_missing = dict()
            for col in self.df.columns.tolist():
                col_missing = pd.isnull(self.df[col])
                fraction_missing[col] = col_missing.mean()
                describe[col] = self.df[col].describe()
            self.summary = {
                "describe": describe,
                "fraction_missing": fraction_missing,
                "shape": self.df.shape,
                "columns": self.df.columns.tolist(),
                "filepath": self.abspath,
            }
        return self.summary


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
        self.valid_ext = VALID_EXT

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
