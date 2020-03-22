"""Class definition for filtering invalid tabular file extensions."""
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
    """Filter file list if non-tabular extensions exist."""

    def __init__(self):
        """Initialize new filter object."""
        super().__init__()
        self.applies_to_available = True
        self.configure()

    def __call__(self, dataset):
        """Perform operation on a tabular dataset.

        :param dataset: dataset to perform file extension filter on
        :type dataset: :class:`kaishi.tabular.dataset.TabularDataset`
        """
        badind = []
        for i in self.get_target_indexes(dataset):
            fobj = dataset.files[i]
            _, ext = os.path.splitext(fobj.basename)
            if len(ext) == 0 or ext not in self.valid_extensions:
                badind.append(i)

        dataset.files, trimmed = trim_list_by_inds(dataset.files, badind)
        dataset.filtered["unsupported_extension"] = trimmed

        return trimmed

    def configure(self, valid_extensions=VALID_EXT):
        """Configure the file extension filter (default list defined in `VALID_EXT`).

        :param valid_extensions: list of file extensions that are valid (each must begin with ".")
        :type valid_extensions: list[str]
        """
        self.valid_extensions = valid_extensions
