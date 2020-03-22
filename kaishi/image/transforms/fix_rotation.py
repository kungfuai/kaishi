"""Class definition for fixing image rotation."""
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.image.labelers.generic_convnet import LabelerGenericConvnet


class TransformFixRotation(PipelineComponent):
    """Fix rotations of each image in a dataset given pre-determined labels (uses the default convnet for labels)."""

    def __init__(self):
        """Initialize new transform component."""
        super().__init__()

    def __call__(self, dataset):
        """Perform the transformation operation on an image dataset.

        :param dataset: image dataset to perform operation on
        :type dataset: :class:`kaishi.image.dataset.ImageDataset`
        """
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
