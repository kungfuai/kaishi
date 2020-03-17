"""Definitions for image file objects and groups of them."""
import warnings
import pandas as pd
from kaishi.core.file import File


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

    def get_summary(self):
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
