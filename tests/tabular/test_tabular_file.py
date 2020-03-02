from kaishi.tabular.file import TabularFile


def test_init():
    test = TabularFile("tests/data", "tabular", "simple.csv")
    assert test.abspath == "tests/data/tabular/simple.csv"


def test_has_csv_file_ext():
    test = TabularFile("tests/data", "tabular", "simple.csv")
    assert test._has_csv_file_ext()
    test.basename = "simple.csv.gz"
    assert test._has_csv_file_ext()
    test.basename = "simple.json"
    assert test._has_csv_file_ext() is False


def test_has_json_file_ext():
    test = TabularFile("tests/data", "tabular", "simple.csv")
    assert test._has_json_file_ext() is False
    test.basename = "simple.json"
    assert test._has_json_file_ext()
    test.basename = "simple.jsonl"
    assert test._has_json_file_ext()
    test.basename = "simple.json.gz"
    assert test._has_json_file_ext()
    test.basename = "simple.jsonl.gz"
    assert test._has_json_file_ext()


def test_verify_loaded():
    test = TabularFile("tests/data", "tabular", "simple.csv")
    assert test.df is None
    test.verify_loaded()
    assert test.df is not None


def test_get_summary():
    test = TabularFile("tests/data", "tabular", "simple.csv")
    summary = test.get_summary()
    assert "describe" in summary.keys()
    assert "describe" in test.summary.keys()
