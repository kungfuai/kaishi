from kaishi.image.file_group import ImageFileGroup


def test_generic_convnet():
    test = ImageFileGroup("tests/data/image", recursive=True)
    test.configure_pipeline(["LabelerGenericConvnet"])
    test.run_pipeline()
    label_count = sum([len(fobj.labels) for fobj in test.files])
    assert label_count > 0
