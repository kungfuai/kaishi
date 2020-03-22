"""Class definition for filtering files with invalid image headers."""
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.core.misc import trim_list_by_inds
from kaishi.image.util import validate_image_header


class FilterInvalidImageHeaders(PipelineComponent):
    """Filter image files that have invalid or nonexistent headers."""

    def __init__(self):
        """Initialize filter object."""
        super().__init__()
        self.applies_to_available = True

    def __call__(self, dataset):
        """Perform filter operation on a kaishi image dataset.

        :param dataset: image dataset to perform filter operation on
        :type dataset: :class:`kaishi.image.dataset.ImageDataset`
        """
        badind = []
        for i in self.get_target_indexes(dataset):
            fobj = dataset.files[i]
            if not validate_image_header(fobj.abspath):
                badind.append(i)

        dataset.files, trimmed = trim_list_by_inds(dataset.files, badind)
        dataset.filtered["invalid_header"] = trimmed
