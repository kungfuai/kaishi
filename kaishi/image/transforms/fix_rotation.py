"""Transforms for image datasets."""
from kaishi.core.labels import Labels
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.image.labelers.generic_convnet import LabelerGenericConvnet


class TransformFixRotation(PipelineComponent):
    """Fix rotations of each image given pre-determined labels."""

    def __init__(self):
        super().__init__()

    def __call__(self, dataset):
        if not dataset.labeled:
            LabelerGenericConvnet()(dataset)
            dataset.labeled = True

        for fobj in dataset.files:
            if fobj.image is None or fobj.has_label("RECTIFIED"):
                continue
            if fobj.has_label("ROTATED_RIGHT"):
                fobj.rotate(90)
                fobj.remove_label("ROTATED_RIGHT")
            elif fobj.has_label("ROTATED_LEFT"):
                fobj.rotate(270)
                fobj.remove_label("ROTATED_LEFT")
            elif fobj.has_label("UPSIDE_DOWN"):
                fobj.rotate(180)
                fobj.remove_label("UPSIDE_DOWN")
            fobj.add_label("RECTIFIED")
