import os
from kaishi.core.labels import Labels
from kaishi.core.file import File


def test_init():
    test = File("tests/data", "image", "sample.jpg")
    assert test.abspath == "tests/data/image/sample.jpg"


def test_str():
    test = File("tests/data", "image", "sample.jpg")
    assert str(test) == "image/sample.jpg"


def test_compute_hash():
    test = File("tests/data", "image", "sample.jpg")
    assert test.compute_hash() == "df11f7053426c06d1c6073f88571ac40"


def test_labels():
    test = File("tests/data", "image", "sample.jpg")
    assert len(test.labels) == 0
    test.add_label(Labels.RECTIFIED)
    assert len(test.labels) == 1
    assert Labels.RECTIFIED in test.labels
    test.remove_label(Labels.RECTIFIED)
    assert len(test.labels) == 0