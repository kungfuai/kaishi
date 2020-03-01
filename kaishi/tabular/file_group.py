"""Definitions for image file objects and groups of them."""
import os
import pandas as pd
from kaishi.core.file_group import FileGroup
from kaishi.core.misc import load_files_by_walk
from kaishi.core.pipeline import Pipeline
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

    def __init__(
        self, source: str, recursive: bool, use_predefined_pipeline: bool = False
    ):
        """Initialize new image file group."""
        super().__init__(recursive)
        self.pipeline = Pipeline()
        self.df_concatenated = None
        self.load_dir(source, TabularFile, recursive)
        if use_predefined_pipeline:
            self.pipeline.configure(["FilterDuplicates"])

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

    def load_all(self):
        for fobj in self.files:
            fobj.verify_loaded()

    def run_pipeline(self, verbose: bool = False):
        """Run the pipeline as configured."""
        self.load_all()
        self.pipeline(self, verbose=verbose)
        if verbose:
            print("Pipeline completed")

    def report(self):
        for i, fobj in enumerate(self.files):
            print(f"\nDataframe {i}")
            print(f"source: {fobj.abspath}")
            print("====================================")
            if fobj.df is None:
                print(f"NO DATA OR NOT LOADED (try running 'dataset.load_all()')")
            else:
                print(fobj.get_summary())
                # print(f"{len(fobj.df.columns)} columns: {list(fobj.df.columns)}")
                # for col in fobj.df.columns:
                #    print(f"\n---  Column '{col}'")
                #    print(fobj.df[col].describe())
            print()
