import os
import tempfile
import pandas as pd
from kaishi.tabular.file import TabularFile
from kaishi.tabular.file_group import TabularFileGroup


def test_init_and_load_dir():
    test = TabularFileGroup("tests/data/tabular", recursive=True)
    assert len(test.files) > 0


def test_constructor_with_predefined_pipeline():
    test = TabularFileGroup(
        "tests/data/tabular", recursive=True, use_predefined_pipeline=True
    )
    print(test.pipeline.components)
    assert len(test.pipeline.components) == 2
    assert test.pipeline.components[0].__class__.__name__ == "FilterDuplicateFiles"


def test_constructor_without_predefined_pipeline():
    test = TabularFileGroup("tests/data/tabular", recursive=True)
    assert len(test.pipeline.components) == 0


def test_load_all():
    test = TabularFileGroup(
        "tests/data/tabular", recursive=True, use_predefined_pipeline=True
    )
    test.load_all()
    found_valid_dataframe = False
    for i in range(len(test.files)):
        if isinstance(test.files[i].df, pd.DataFrame):
            found_valid_dataframe = True
    assert found_valid_dataframe


def test_save():
    test = TabularFileGroup(
        "tests/data/tabular", recursive=True, use_predefined_pipeline=True
    )
    test.load_all()
    tempdir = tempfile.TemporaryDirectory()
    test.save(tempdir.name)
    assert len(os.listdir(tempdir.name)) > 0
