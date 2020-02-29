"""Filters for image datasets."""
import os
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.core.misc import trim_list_by_inds
from kaishi.image.util import validate_image_header


class FilterInvalidImageHeaders(PipelineComponent):
    """Filter file list if image files have invalid or nonexistent header."""

    def __init__(self, dataset):
        super().__init__(dataset)

    def __call__(self):
        badind = []
        for i in self.get_target_indexes():
            fobj = self.dataset.files[i]
            if not validate_image_header(fobj.abspath):
                badind.append(i)

        self.dataset.files, trimmed = trim_list_by_inds(self.dataset.files, badind)
        self.dataset.filtered["invalid_header"] = trimmed

        return trimmed
