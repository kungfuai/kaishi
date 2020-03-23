import os
import tempfile
from kaishi.image.file_group import ImageFileGroup


def test_init_and_load_dir():
    test = ImageFileGroup("tests/data/image", recursive=True)
    assert len(test.files) > 0


def test_load_all():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.load_all()
    assert sum([fobj.image is not None for fobj in test.files]) > 0


def test_save():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.load_all()
    tempdir = tempfile.TemporaryDirectory()
    test.save(tempdir.name)
    assert len(os.listdir(tempdir.name)) > 0
