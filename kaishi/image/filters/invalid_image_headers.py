"""Filters for image datasets."""
import os
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.core.misc import trim_list_by_inds
from kaishi.image.util import validate_image_header


class FilterInvalidImageHeaders(PipelineComponent):
    """Filter file list if image files have invalid or nonexistent header."""

    def __init__(self):
        super().__init__()
        self.applies_to_available = True

    def __call__(self, dataset):
        badind = []
        for i in self.get_target_indexes(dataset):
            fobj = dataset.files[i]
            if not validate_image_header(fobj.abspath):
                badind.append(i)

        dataset.files, trimmed = trim_list_by_inds(dataset.files, badind)
        dataset.filtered["invalid_header"] = trimmed

        return trimmed
