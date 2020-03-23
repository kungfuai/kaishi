"""Class definition for group of tabular files."""
import os
from kaishi.core.file_group import FileGroup
from kaishi.core.pipeline import Pipeline
from kaishi.tabular.file import TabularFile


class TabularFileGroup(FileGroup):
    """Object containing groups of :class:`kaishi.tabular.file.File` objects with methods to perform common operations on them."""

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
    from kaishi.tabular.aggregators.concatenate_dataframes import (
        AggregatorConcatenateDataframes,
    )

    def __init__(
        self,
        source: str,
        recursive: bool,
        use_predefined_pipeline: bool = False,
        out_dir: str = None,
    ):
        """Initialize new tabular file group and a data processing pipeline.

        :param source: The path to the folder where the tabular data (csv or json files) are stored.
        :type source: str
        :param recursive: If True, Traverse the folder recursively to find files.
        :type recursive: bool
        :param use_predefined_pipeline: If True, use a predefined pipeline: load -> concat -> dedup -> export.
        :type use_predefined_pipeline: bool
        :param out_dir: The output directory.
        :type out_dir: str
        """
        super().__init__(recursive)
        self.pipeline = Pipeline()
        self.artifacts["df_concatenated"] = None
        self.load_dir(source, TabularFile, recursive)
        if use_predefined_pipeline:
            if out_dir is not None:

                def save():
                    self.save(out_dir=out_dir)

                self.configure_pipeline(
                    ["FilterDuplicateFiles", "FilterDuplicateRowsEachDataframe", save]
                )
            self.configure_pipeline(
                ["FilterDuplicateFiles", "FilterDuplicateRowsEachDataframe"]
            )

    def _get_indexes_with_valid_dataframe(self):
        """Get a list of indexes with valid dataframes.

        :return: indexes with valid dataframe
        :rtype: list
        """
        valid_indexes = []
        for i, fobj in enumerate(self.files):
            fobj.verify_loaded()
            if fobj.df is not None:
                valid_indexes.append(i)

        return valid_indexes

    def _get_valid_dataframes(self):
        """Get a list of valid dataframe objects.

        :return: valid dataframes
        :rtype: list[:class:`pandas.core.frame.DataFrame`]
        """
        valid_indexes = self._get_indexes_with_valid_dataframe()
        return [self.files[i].df for i in valid_indexes]

    def save(self, out_dir: str, file_format: str = "csv"):
        """Save the processed dataset as individual files or as one file with all the data.

        :param out_dir: The path of the output directory. If the directory does not exist, it will be created.
        :type out_dir: str
        :param file_format: The format of output files. Currently only supports "csv".
        :type file_format: str
        """
        print(f"Saving the results to {out_dir}")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        if self.artifacts["df_concatenated"] is not None:
            if file_format == "csv":
                self.artifacts["df_concatenated"].to_csv(
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
        """Load all files from the source directory."""
        for fobj in self.files:
            fobj.verify_loaded()

    def run_pipeline(self, verbose: bool = False):
        """Run the pipeline as configured.

        :param verbose: flag indicating verbosity
        :type verbose: bool
        """
        self.load_all()
        self.pipeline(self, verbose=verbose)
        if verbose:
            print("Pipeline completed")

    def report(self):
        # TODO: Also do missing fraction reporting on the file group level.
        """Print a report of the dataset in its current state."""
        for i, fobj in enumerate(self.files):
            print(f"\nDataframe {i}")
            print(f"source: {fobj.abspath}")
            print("====================================")
            if fobj.df is None:
                print(f"NO DATA OR NOT LOADED (try running 'dataset.load_all()')")
            else:
                # print(fobj.get_summary())
                print(f"{len(fobj.df.columns)} columns: {list(fobj.df.columns)}")
                for col in fobj.df.columns:
                    print(f"\n---  Column '{col}'")
                    print(fobj.df[col].describe())
                print("\n***** Fraction of missing data in each column *****")
                fraction_missing = fobj.get_summary()["fraction_missing"]
                for col in fobj.df.columns:
                    print(f"{col}: {fraction_missing[col]}")
            print()
