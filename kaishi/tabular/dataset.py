"""Data exploration utilities for tabular data (csv files, database tables).
"""
from glob import glob
import os
import pandas as pd
from kaishi.core.pipeline import Pipeline
from kaishi.tabular.file_group import TabularFileGroup


class TabularDataset:
    def __new__(
        self,
        source: str = None,
        recursive: bool = False,
        use_predefined_pipeline: bool = False,
    ):
        if os.path.exists(source):
            return TabularFileGroup(
                source=source,
                recursive=recursive,
                use_predefined_pipeline=use_predefined_pipeline,
            )
        else:
            raise NotImplementedError("Currently only supports a valid path as input")
