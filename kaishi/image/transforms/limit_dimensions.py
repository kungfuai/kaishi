"""Class definition for limiting the max dimension of each image in an image dataset."""
from kaishi.core.pipeline_component import PipelineComponent


class TransformLimitDimensions(PipelineComponent):
    """Transform to limit max dimension of each image in a dataset."""

    def __init__(self):
        """Initialize new transform object."""
        super().__init__()
        self.applies_to_available = True
        self.configure()

    def __call__(self, dataset):
        """Perform operation on a specified dataset.

        :param dataset: image dataset to perform operation on
        :type dataset: :class:`kaishi.image.dataset.ImageDatset`
        """
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
        """Configure the component. Any combination of these parameters can be defined or not, where smallest
        specified max value in each case is the assumed value (e.g. if `max_width` is 300 but `max_dimension`
        is 200, the maximum width is effectively 200).

        :param max_dimension: maximum dimension for each image (either width or height)
        :type max_dimension: int
        :param max_width: maximum width for each image
        :type max_width: int
        :param max_height: maximum height for each image
        :type max_height: int
        """
        self.max_dimension = max_dimension
        self.max_width = max_width
        self.max_height = max_height
