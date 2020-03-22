"""Class definition for filtering by invalid image file extensions."""
import os
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.core.misc import trim_list_by_inds


VALID_EXT = [  # Valid extensions for invalid file extension filter
    ".bmp",
    ".dib",
    ".jpeg",
    ".jpg",
    ".jpe",
    ".jp2",
    ".png",
    ".pbm",
    ".pgm",
    ".ppm",
    ".sr",
    ".ras",
    ".tiff",
    ".tif",
]


class FilterInvalidFileExtensions(PipelineComponent):
    """Filter files without a valid image file extension, where valid extensions are defined in the `configure` method."""

    def __init__(self):
        """Initialize new filter component."""
        super().__init__()
        self.applies_to_available = True
        self.configure()

    def __call__(self, dataset):
        """Perform the filter operation on `dataset`.

        :param dataset: dataset to perform filter operation on
        :type dataset: :class:`kaishi.image.dataset.ImageDataset`
        """
        # Trim any files without image extensions
        badind = []
        for i in self.get_target_indexes(dataset):
            fobj = dataset.files[i]
            _, ext = os.path.splitext(fobj.basename)
            if len(ext) == 0 or ext.lower() not in self.valid_extensions:
                badind.append(i)

        dataset.files, trimmed = trim_list_by_inds(dataset.files, badind)
        dataset.filtered["unsupported_extension"] = trimmed

    def configure(self, valid_extensions=VALID_EXT):
        """Configure filter with the valid extensions defined.

        :param valid_extensions: list of valid extensions (each should start with ".")
        :type valid_extensions: list[str]
        """
        self.valid_extensions = valid_extensions
