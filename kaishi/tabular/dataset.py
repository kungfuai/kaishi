"""Data exploration utilities for tabular data (csv files, database tables).
"""
from glob import glob
import os
import warnings
import pandas as pd
from kaishi.core.pipeline import Pipeline
from kaishi.tabular.file import TabularFileGroup


class TabularDataset(TabularFileGroup):
    def __init__(
        self,
        source: str,
        source_type: str = "directory",
        recursive: bool = False,
        use_predefined_pipeline: bool = False,
    ):
        super().__init__(recursive=recursive)
        # Construct a pipeline.
        if source_type != "directory":
            raise NotImplementedError
        self.source = source
        self.source_type = source_type
        self.pipeline = Pipeline()
        if self.source is not None:
            if os.path.exists(source):
                self.load_dir(source)
            else:
                warnings.warn("Directory not found, initializing empty Dataset")

    def load_all(self):
        for fobj in self.files:
            fobj.verify_loaded()

    def run(self, verbose: bool = False):
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
                print(f"{len(fobj.df.columns)} columns: {list(fobj.df.columns)}")
                for col in fobj.df.columns:
                    print(f"\n---  Column '{col}'")
                    print(fobj.df[col].describe())
            print()
