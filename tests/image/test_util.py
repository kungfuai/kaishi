from kaishi.image.util import validate_image_header


def test_validate_image_header():
    invalid_file = "tests/data/image/empty_unsupported_extension.gif"
    valid_file = "tests/data/image/sample.jpg"
    assert validate_image_header(invalid_file) is False
    assert validate_image_header(valid_file) is True
