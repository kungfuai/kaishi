from kaishi.core.file import File
from kaishi.core.file_group import FileGroup


def test_by_regex():
    test = FileGroup(recursive=True)
    test.load_dir("tests/data/image", File, recursive=True)
    test.configure_pipeline(["FilterByRegex"])
    test.pipeline.components[0].configure(pattern="sample.jpg")
    original_count = len(test.files)
    test.run_pipeline()
    assert len(test.files) == original_count - 1


def test_by_label():
    test = FileGroup(recursive=True)
    test.load_dir("tests/data/image", File, recursive=True)
    test.configure_pipeline(["FilterByLabel"])
    test.pipeline.components[0].configure(label_to_filter="TRAIN")
    test.files[0].add_label("TRAIN")
    original_count = len(test.files)
    test.run_pipeline()
    assert len(test.files) == original_count - 1


def test_subsample():
    test = FileGroup(recursive=True)
    test.load_dir("tests/data/image", File, recursive=True)
    test.configure_pipeline(["FilterSubsample"])
    assert len(test.files) > 2
    test.pipeline.components[0].configure(N=2)
    test.run_pipeline()
    assert len(test.files) == 2
