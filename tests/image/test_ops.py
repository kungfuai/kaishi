import PIL
from kaishi.image.ops import (
    extract_patch,
    make_small,
    add_jpeg_compression,
    add_rotation,
    add_stretching,
    add_poisson_noise,
)


test_image = PIL.Image.open("tests/data/image/sample.jpg")


def test_extract_patch():
    patch = extract_patch(test_image, (10, 10))
    assert patch.size[0] == 10 and patch.size[1] == 10


def test_make_small():
    small = make_small(test_image, max_dim=224)
    assert max(small.size) == 224


def test_add_jpeg_compression():
    compressed = add_jpeg_compression(test_image)
    assert len(compressed.size) == 2


def test_add_rotation():
    rotated = add_rotation(test_image, ccw_rotation_degrees=90)
    assert (
        test_image.size[0] == rotated.size[1] and test_image.size[1] == rotated.size[0]
    )


def test_add_stretching():
    stretched = add_stretching(test_image, 100, 100)
    assert (
        stretched.size[0] == 2 * test_image.size[0]
        and stretched.size[1] == 2 * test_image.size[1]
    )


def test_add_poisson_noise():
    noisy = add_poisson_noise(test_image)
    assert len(noisy.size) == 2
