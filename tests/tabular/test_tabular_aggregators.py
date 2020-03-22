import pytest
from kaishi.tabular.file_group import TabularFileGroup


def test_concatenate_dataframes():
    test = TabularFileGroup("tests/data/tabular", recursive=True)
    test.configure_pipeline(["AggregatorConcatenateDataframes"])
    test.pipeline.components[0].applies_to("simple.csv|to_concatenate.csv")
    with pytest.warns(UserWarning):
        test.run_pipeline()
    assert len(test.artifacts["df_concatenated"]) == 8
