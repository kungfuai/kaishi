"""Filters for image datasets."""
import os
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.misc import find_similar_by_value
from kaishi.image.util import validate_image_header


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


class FilterSimilar(PipelineComponent):
    """Filter near duplicate files, detected via perceptual hashing ('imagehash' library)."""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.configure()

    def __call__(self):
        hashlist = [
            f.perceptual_hash
            if f.perceptual_hash is not None
            else f.compute_perceptual_hash()
            for f in self.dataset.files
        ]

        duplicate_ind, parent_ind = find_similar_by_value(
            hashlist, self.perceptual_hash_threshold
        )
        for di, pi in zip(duplicate_ind, parent_ind):
            self.dataset.files[pi].children["similar"].append(self.dataset.files[di])
        self.dataset.files, trimmed = trim_list_by_inds(
            self.dataset.files, duplicate_ind
        )
        self.dataset.filtered["similar"] = trimmed

        return trimmed

    def configure(self, perceptual_hash_threshold=3):
        self.perceptual_hash_threshold = perceptual_hash_threshold


class FilterInvalidFileExtensions(PipelineComponent):
    """Filter file list if non-image extensions exist."""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.configure()

    def __call__(self):
        # Trim any files without image extensions
        badind = []
        for i, fobj in enumerate(self.dataset.files):
            _, ext = os.path.splitext(fobj.basename)
            if len(ext) == 0 or ext.lower() not in self.valid_extensions:
                badind.append(i)

        self.dataset.files, trimmed = trim_list_by_inds(self.dataset.files, badind)
        self.dataset.filtered["unsupported_extension"] = trimmed

        return trimmed

    def configure(self, valid_extensions=VALID_EXT):
        self.valid_extensions = valid_extensions


class FilterInvalidImageHeaders(PipelineComponent):
    """Filter file list if image files have invalid or nonexistent header."""

    def __init__(self, dataset):
        super().__init__(dataset)

    def __call__(self):
        badind = []
        for i, fobj in enumerate(self.dataset.files):
            if not validate_image_header(fobj.abspath):
                badind.append(i)

        self.dataset.files, trimmed = trim_list_by_inds(self.dataset.files, badind)
        self.dataset.filtered["invalid_header"] = trimmed

        return trimmed
