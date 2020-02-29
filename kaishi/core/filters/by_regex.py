"""Core filters for multiple dataset types."""
import re
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.pipeline_component import PipelineComponent


class FilterByRegex(PipelineComponent):
    """Filter duplicate files, detected via hashing."""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.configure()

    def __call__(self):

        to_trim = []
        for i in self.get_target_indexes():
            if re.match(self.pattern, str(self.dataset.files[i])):
                to_trim.append(i)
        self.dataset.files, trimmed = trim_list_by_inds(self.dataset.files, to_trim)
        self.dataset.filtered["regex"] = trimmed

        return trimmed

    def configure(self, pattern="/(?=a)b/"):
        """Default configuration returns false always."""
        self.pattern = pattern
