"""Class definition for transforming images to grayscale."""
from kaishi.core.pipeline_component import PipelineComponent


class TransformToGrayscale(PipelineComponent):
    """Transform images in a dataset to grayscale."""

    def __init__(self):
        """Initialize transform component."""
        super().__init__()
        self.applies_to_available = True

    def __call__(self, dataset):
        """Perform operation on a given dataset.

        :param dataset: image dataset with images to convert
        :type dataset: :class:`kaishi.image.dataset.ImageDataset`
        """
        for i in self.get_target_indexes(dataset):
            dataset.files[i].convert_to_grayscale()
