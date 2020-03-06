from kaishi.core.labels import Labels
from kaishi.image.file_group import ImageFileGroup


def test_fix_rotation():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.configure_pipeline(["TransformFixRotation"])
    test.run_pipeline()
    found_rectified = False
    found_rotated = False
    for fobj in test.files:
        if fobj.has_label("RECTIFIED"):
            found_rectified = True
        if fobj.has_label("ROTATED_LEFT"):
            found_rotated = True
        if fobj.has_label("ROTATED_RIGHT"):
            found_rotated = True
        if fobj.has_label("UPSIDE_DOWN"):
            found_rotated = True
    assert found_rectified is True and found_rotated is False
