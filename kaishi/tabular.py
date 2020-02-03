"""Data exploration utilities for tabular data (csv files, database tables).
"""
from glob import glob
from os import path
import pandas as pd

from kaishi.util.pipeline import Pipeline


class TabularDataInspector:
    def __init__(
        self,
        source: str,
        source_type: str = "directory",
        recursive: bool = False,
        use_predefined_pipeline: bool = False,
    ):
        """
        Construct an inspector for tabular data. It can be
        - a diretory of files, csv, json line, json,
        - a connection str compatible with sqlalchemy (not implemented yet).

        Parameters
        ----------
        source: str
            A path to a directory.
        source_type: str
            One of "directory", "connection_string".
        """
        # Construct a pipeline.
        if recursive:
            raise NotImplementedError
        if source_type != "directory":
            raise NotImplementedError
        self.source = source
        self.source_type = source_type
        self.recursive = recursive
        self.files = []
        self.pipeline = Pipeline()
        if use_predefined_pipeline:
            self.pipeline.add_component(self.load)
            self.pipeline.add_component(self.print)

    def _has_csv_file_ext(self, f):
        f = f.lower()
        return f.endswith(".csv.gz") or f.endswith(".csv")

    def _has_json_file_ext(self, f):
        f = f.lower()
        return (
            f.endswith(".json")
            or f.endswith(".jsonl")
            or f.endswith(".json.gz")
            or f.endswith(".jsonl.gz")
        )

    def load(self):
        print("[tabular load]")
        dfs = []
        if self.source_type == "directory":
            for f in glob(path.join(self.source, "*")):
                if self._has_csv_file_ext(f):
                    self.files.append(f)
                    dfs.append(pd.read_csv(f))
                elif self._has_json_file_ext(f):
                    self.files.append(f)
                    dfs.append(pd.read_json(f))
        else:
            raise ValueError("source_type {} not supported.".format(self.source_type))
        self.dfs = dfs

        # TODO: decide whether and which dataframes to concat.

        self.df_summaries = []
        for df, filepath in zip(self.dfs, self.files):
            fraction_missing = {}
            describe = {}
            for col in df.columns.tolist():
                col_missing = pd.isnull(df[col])
                fraction_missing[col] = col_missing.mean()
                describe[col] = df[col].describe()
            self.df_summaries.append(
                dict(
                    describe=describe,
                    fraction_missing=fraction_missing,
                    shape=df.shape,
                    columns=df.columns.tolist(),
                    filepath=filepath,
                )
            )

    def print(self):
        for i, s in enumerate(self.df_summaries):
            print(f"\nDataframe {i}. Shape = {s['shape']}")
            print(f"source: {s['filepath']}")
            print("====================================")
            print(f"{len(s['columns'])} columns:", s["columns"])
            for col in s["columns"]:
                print(f"\n---  Column {col}")
                print(s["describe"][col])
                print(f"Fraction of missing values: {s['fraction_missing'][col]}.")

    def concatenate_all(self):
        # concat all tables.
        self.df_concatenated = pd.concat(self.dfs).reset_index(drop=True)

    @property
    def is_concatenated(self):
        return hasattr(self, "df_concatenated")

    def dedup(self, columns=None, concatenate=False):
        if concatenate:
            if not self.is_concatenated:
                self.concatenate_all()
            self.df_concatenated.drop_duplicates(inplace=True)
        else:
            for df in self.dfs:
                df.drop_duplicates(inplace=True)

    def save(self, out_dir, max_rows_per_file=1e6):
        if self.is_concatenated:
            self.df_concatenated.to_csv(path.join(out_dir, "all.csv"), index=False)
        else:
            for df, filepath in zip(self.dfs, self.files):
                filename = path.basename(file)
                if not filename.lower().endswith(".csv"):
                    filename += ".csv"
                df.to_csv(path.join(out_dir, filename))

    def run_pipeline(self, verbose=False):
        # It is using the same method name as in `image.Dataset`.
        self.pipeline.run()
        if verbose:
            print("Pipeline completed")
