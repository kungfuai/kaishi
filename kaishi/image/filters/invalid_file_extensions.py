"""Filter invalid file extensions."""
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
    """Filter file list if non-image extensions exist."""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.configure()

    def __call__(self):
        # Trim any files without image extensions
        badind = []
        for i in self.get_target_indexes():
            fobj = self.dataset.files[i]
            _, ext = os.path.splitext(fobj.basename)
            if len(ext) == 0 or ext.lower() not in self.valid_extensions:
                badind.append(i)

        self.dataset.files, trimmed = trim_list_by_inds(self.dataset.files, badind)
        self.dataset.filtered["unsupported_extension"] = trimmed

        return trimmed

    def configure(self, valid_extensions=VALID_EXT):
        self.valid_extensions = valid_extensions
