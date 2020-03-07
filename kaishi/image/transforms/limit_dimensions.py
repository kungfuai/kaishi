"""Limit the max size of all images."""
from kaishi.core.pipeline_component import PipelineComponent


class TransformLimitDimensions(PipelineComponent):
    """Transform to limit max dimension of each image in a dataset."""

    def __init__(self):
        super().__init__()
        self.applies_to_available = True
        self.configure()

    def __call__(self, dataset):
        if all(
            [
                self.max_dimension is None,
                self.max_width is None,
                self.max_height is None,
            ]
        ):
            return
        for i in self.get_target_indexes(dataset):
            dataset.files[i].limit_dimensions(
                max_dimension=self.max_dimension,
                max_width=self.max_width,
                max_height=self.max_height,
            )

    def configure(self, max_dimension=None, max_width=None, max_height=None):
        self.max_dimension = max_dimension
        self.max_width = max_width
        self.max_height = max_height
