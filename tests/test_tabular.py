import pytest

from kaishi.tabular import TabularDataInspector, pd


class TestTabularDataInspector:
    # TODO: add tests for dedup and missing data fraction.
    def test_constructor_with_predefined_pipeline(self):
        tdi = TabularDataInspector("sample_data/simple_csv", use_predefined_pipeline=True)
        assert len(tdi.pipeline.components) == 4
        assert tdi.pipeline.components[0] == tdi.load

    def test_constructor_without_predefined_pipeline(self):
        tdi = TabularDataInspector("sample_data/simple_csv", use_predefined_pipeline=False)
        assert len(tdi.pipeline.components) == 0

    def test_load_simple_csv(self):
        tdi = TabularDataInspector("sample_data/simple_csv", use_predefined_pipeline=False)
        tdi.load()
        assert len(tdi.dfs) == 1
        assert isinstance(tdi.dfs[0], pd.DataFrame)

    def test_save_simple_csv(self, tmpdir):
        tdi = TabularDataInspector("sample_data/simple_csv", use_predefined_pipeline=False)
        tdi.load()
        output_dir = tmpdir.mkdir("output")
        tdi.save(output_dir)
        fn = tmpdir.join("output", "0.csv")
        assert fn.isfile()
        df = pd.read_csv(fn)
        assert df.shape == (3, 3)
