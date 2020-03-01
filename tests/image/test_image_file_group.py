import os
import tempfile
from kaishi.image.file import ImageFile
from kaishi.image.file_group import ImageFileGroup


def test_init_and_load_dir():
    test = ImageFileGroup("tests/data/image", recursive=True)
    assert len(test.files) > 0


def test_load_instance_when_none():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test_file = ImageFile("tests/data", "image", "empty_unsupported_extension.gif")
    test.load_instance(test_file)
    assert test_file.image is None


def test_load_instance_when_not_none():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test_file = ImageFile("tests/data", "image", "sample.jpg")
    test.load_instance(test_file)
    assert test_file.image is not None


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
