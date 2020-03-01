from io import StringIO
import os
import tempfile
import sys
from kaishi.core.file import File
from kaishi.core.file_group import FileGroup


def test_init_and_load_dir():
    test = FileGroup(recursive=True)
    test.load_dir("tests/data/image", File, True)
    assert len(test.files) > 0


def test_get_pipeline_options():
    test = FileGroup(recursive=True)
    assert len(test.get_pipeline_options()) > 0


def test_configure_pipeline():
    test = FileGroup(recursive=True)
    test.configure_pipeline(["FilterDuplicateFiles"])
    pipeline_names = [
        component.__class__.__name__ for component in test.pipeline.components
    ]
    assert "FilterDuplicateFiles" in pipeline_names


def test_file_report():
    test = FileGroup(recursive=True)
    test.load_dir("tests/data/image", File, True)
    print_capture = StringIO()
    sys.stdout = print_capture
    test.file_report()
    sys.stdout = sys.__stdout__
    assert "sample.jpg" in print_capture.getvalue()
