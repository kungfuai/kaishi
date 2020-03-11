from kaishi.core.file import File
from kaishi.core.file_group import FileGroup


def test_validation_and_test():
    test = FileGroup(recursive=True)
    test.load_dir("tests/data", File, recursive=True)
    test.configure_pipeline(["LabelerValidationAndTest"])
    test.pipeline.components[0].configure(val_frac=0.2, test_frac=0.2)
    test.run_pipeline()
    found_counts = [0, 0, 0]
    for fobj in test.files:
        if fobj.has_label("TRAIN"):
            found_counts[0] += 1
        elif fobj.has_label("VALIDATE"):
            found_counts[1] += 1
        elif fobj.has_label("TEST"):
            found_counts[2] += 1

    assert found_counts[0] == len(test.files) - 2 * round(len(test.files) * 0.2)
    assert found_counts[1] == round(len(test.files) * 0.2)
    assert found_counts[2] == round(len(test.files) * 0.2)
