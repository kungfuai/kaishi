"""Class definition for data exploration utilities for tabular data (csv files, database tables)."""
import os
from kaishi.tabular.file_group import TabularFileGroup


class TabularDataset:
    """Object for analyzing and manipulating tabular datasets."""

    def __new__(
        self,
        source: str = None,
        recursive: bool = False,
        use_predefined_pipeline: bool = False,
        out_dir: str = None,
    ):
        """Create a tabular data object given a directory of files.

        :param source: The path to the folder where the tabular data (csv or json files) are stored.
        :type source: str
        :param recursive: If True, Traverse the folder recursively to find files.
        :type recursive: bool
        :param use_predefined_pipeline: If True, use a predefined pipeline: load -> concat -> dedup -> export.
        :type use_predefined_pipeline: bool
        :param out_dir: The output directory.
        :type out_dir: str
        """
        if os.path.exists(source):
            return TabularFileGroup(
                source=source,
                recursive=recursive,
                use_predefined_pipeline=use_predefined_pipeline,
                out_dir=out_dir,
            )
        else:
            raise NotImplementedError("Currently only supports a valid path as input")
