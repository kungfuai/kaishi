from kaishi.image.file import ImageFile


def test_init():
    test = ImageFile("tests/data", "image", "sample.jpg")
    assert test.abspath == "tests/data/image/sample.jpg"


def test_verify_loaded():
    test = ImageFile("tests/data", "image", "sample.jpg")
    test.verify_loaded()
    assert test.image is not None
    assert test.thumbnail is not None
    assert test.small_image is not None
    assert test.patch is not None


def test_rotate():
    test = ImageFile("tests/data", "image", "sample.jpg")
    test.verify_loaded()
    original_size = test.image.size
    test.rotate(90)
    assert (
        test.image.size[0] == original_size[1]
        and test.image.size[1] == original_size[0]
    )


def test_compute_perceptual_hash():
    test = ImageFile("tests/data", "image", "sample.jpg")
    hashval = test.compute_perceptual_hash()
    assert str(hashval) == "00302df7d7978303"
