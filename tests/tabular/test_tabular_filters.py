import pytest
import warnings
from kaishi.tabular.file_group import TabularFileGroup


def test_invalid_file_extensions():
    test = TabularFileGroup("tests/data/tabular", recursive=True)
    test.configure_pipeline(["FilterInvalidFileExtensions"])
    test.run_pipeline()
    assert len(test.filtered["unsupported_extension"]) > 0


def test_duplicate_rows_after_concatenation():
    test = TabularFileGroup("tests/data/tabular", recursive=True)
    test.configure_pipeline(["FilterDuplicateRowsAfterConcatenation"])
    test.run_pipeline()
    assert len(test.df_concatenated) == 7


def test_duplicate_rows_each_file():
    test = TabularFileGroup("tests/data/tabular", recursive=True)
    test.configure_pipeline(["FilterDuplicateRowsEachDataframe"])
    test.pipeline.components[0].applies_to("simple.csv")
    with pytest.warns(UserWarning):
        test.load_all()
    for i in range(len(test.files)):
        if str(test.files[i]) == "simple.csv":
            break
    assert len(test.files[i].df) == 4
    with pytest.warns(UserWarning):
        test.run_pipeline()
    assert len(test.files[i].df) == 3
