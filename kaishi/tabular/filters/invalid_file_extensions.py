"""Filters for image datasets."""
import os
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.core.misc import trim_list_by_inds


VALID_EXT = [
    ".json",
    ".jsonl",
    ".json.gz",
    ".jsonl.gz",
    ".csv",
    ".csv.gz",
]


class FilterInvalidFileExtensions(PipelineComponent):
    """Filter file list if non-image extensions exist."""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.configure()

    def __call__(self):
        badind = []
        for i in self.get_target_indexes():
            fobj = self.files[i]
            _, ext = os.path.splitext(fobj.basename)
            if len(ext) == 0 or ext not in self.valid_extensions:
                badind.append(i)

        self.dataset.files, trimmed = trim_list_by_inds(self.dataset.files, badind)
        self.dataset.filtered["unsupported_extension"] = trimmed

        return trimmed

    def configure(valid_extensions=VALID_EXT):
        self.valid_extensions = valid_ext
