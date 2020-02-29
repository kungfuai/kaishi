"""Filters for image datasets."""
import os
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.core.misc import trim_list_by_inds


class FilterInvalidFileExtensions(PipelineComponent):
    """Filter file list if non-image extensions exist."""

    def __init__(self, dataset):
        super().__init__(dataset)

    def __call__(self):
        badind = []
        for i, fobj in enumerate(self.dataset.files):
            _, ext = os.path.splitext(fobj.basename)
            if len(ext) == 0 or ext not in self.dataset.valid_ext:
                badind.append(i)

        self.dataset.files, trimmed = trim_list_by_inds(self.dataset.files, badind)
        self.dataset.filtered["unsupported_extension"] = trimmed

        return trimmed
