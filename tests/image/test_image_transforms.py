from kaishi.image.file_group import ImageFileGroup


def test_to_grayscale():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.configure_pipeline(["TransformToGrayscale"])
    test.load_all()
    test_ind = 0
    while repr(test.files[test_ind]) != "sample.jpg":
        test_ind += 1
    assert test.files[test_ind].image.mode != "L"
    test.run_pipeline()
    assert test.files[test_ind].image.mode == "L"


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


def test_limit_dimensions():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.configure_pipeline(["TransformLimitDimensions"])
    test.pipeline.components[0].configure(max_dimension=100)
    test.run_pipeline()
    heights = [fobj.image.size[0] for fobj in test.files if fobj.image]
    widths = [fobj.image.size[0] for fobj in test.files if fobj.image]
    assert len(test.files) > 0
    assert max([max(widths), max(heights)]) == 100


def test_limit_dimensions_width_only():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.configure_pipeline(["TransformLimitDimensions"])
    test.pipeline.components[0].configure(max_width=100)
    test.run_pipeline()
    widths = [fobj.image.size[0] for fobj in test.files if fobj.image]
    assert len(test.files) > 0
    assert max(widths) == 100


def test_limit_dimensions_height_only():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.configure_pipeline(["TransformLimitDimensions"])
    test.pipeline.components[0].configure(max_height=100)
    test.run_pipeline()
    heights = [fobj.image.size[1] for fobj in test.files if fobj.image]
    assert len(test.files) > 0
    assert max(heights) == 100


def test_limit_dimensions_no_setting():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.configure_pipeline(["TransformLimitDimensions"])
    test.load_all()
    heights_before = [fobj.image.size[0] for fobj in test.files if fobj.image]
    widths_before = [fobj.image.size[0] for fobj in test.files if fobj.image]
    test.run_pipeline()
    heights_after = [fobj.image.size[0] for fobj in test.files if fobj.image]
    widths_after = [fobj.image.size[0] for fobj in test.files if fobj.image]
    assert len(test.files) > 0
    assert sum(heights_before) == sum(heights_after)
    assert sum(widths_before) == sum(widths_after)
