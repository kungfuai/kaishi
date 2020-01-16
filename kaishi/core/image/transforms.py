from kaishi.util.labels import Labels
from kaishi.core.image.labelers import LabelerMacro


class TransformFixRotation:
    """Fix rotations of each image given pre-determined labels."""

    def __init__(self, dataset):
        self.dataset = dataset

    def __call__(self):
        if not self.dataset.labeled:
            labeler = LabelerMacro(self.dataset)
            labeler()
            self.dataset.labeled = True

        for f in self.dataset.files:
            if Labels.RECTIFIED in f.labels:
                continue
            elif Labels.ROTATED_RIGHT in f.labels:
                f.rotate(90)
                f.remove_label(Labels.ROTATED_RIGHT)
            elif Labels.ROTATED_LEFT in f.labels:
                f.rotate(270)
                f.remove_label(Labels.ROTATED_LEFT)
            elif Labels.UPSIDE_DOWN in f.labels:
                f.rotate(180)
                f.remove_label(Labels.UPSIDE_DOWN)
            f.add_label(Labels.RECTIFIED)
