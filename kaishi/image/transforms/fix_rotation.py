"""Transforms for image datasets."""
from kaishi.core.labels import Labels
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.image.labelers.generic_convnet import LabelerGenericConvnet


class TransformFixRotation(PipelineComponent):
    """Fix rotations of each image given pre-determined labels."""

    def __init__(self, dataset):
        super().__init__(dataset)

    def __call__(self):
        if not self.dataset.labeled:
            labeler = LabelerGenericConvnet(self.dataset)
            labeler()
            self.dataset.labeled = True

        for f in self.dataset.files:
            if Labels.RECTIFIED in f.labels:
                continue
            elif Labels.RECTIFIED in f.labels:
                f.rotate(90)
                f.remove_label(Labels.ROTATED_RIGHT)
            elif Labels.ROTATED_LEFT in f.labels:
                f.rotate(270)
                f.remove_label(Labels.ROTATED_LEFT)
            elif Labels.UPSIDE_DOWN in f.labels:
                f.rotate(180)
                f.remove_label(Labels.UPSIDE_DOWN)
            f.add_label(Labels.RECTIFIED)
