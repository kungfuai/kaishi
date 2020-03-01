from kaishi.image.file_group import ImageFileGroup


def test_invalid_file_extensions():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.configure_pipeline(["FilterInvalidFileExtensions"])
    test.run_pipeline()
    assert len(test.filtered["unsupported_extension"]) > 0


def test_invalid_image_headers():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.configure_pipeline(["FilterInvalidImageHeaders"])
    test.run_pipeline()
    assert len(test.filtered["invalid_header"]) > 0


def test_similar():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.configure_pipeline(["FilterSimilar"])
    test.run_pipeline()
    assert len(test.filtered["similar"]) > 0
