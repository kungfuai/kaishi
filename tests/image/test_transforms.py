from kaishi.core.labels import Labels
from kaishi.image.file_group import ImageFileGroup


def test_fix_rotation():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.configure_pipeline(["TransformFixRotation"])
    test.run_pipeline()
    found_rectified = False
    found_rotated = False
    for fobj in test.files:
        if Labels.RECTIFIED in fobj.labels:
            found_rectified = True
        if Labels.ROTATED_LEFT in fobj.labels:
            found_rotated = True
        if Labels.ROTATED_RIGHT in fobj.labels:
            found_rotated = True
        if Labels.UPSIDE_DOWN in fobj.labels:
            found_rotated = True
    assert found_rectified is True and found_rotated is False
