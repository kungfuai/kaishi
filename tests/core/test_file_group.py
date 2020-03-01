import os
import tempfile
from kaishi.core.file import File
from kaishi.core.file_group import FileGroup


def test_init_and_load_dir():
    test = FileGroup(recursive=True)
    test.load_dir("tests/data/image", File, True)
    assert len(test.files) > 0
