"""Class definition for filter by regex."""
import re
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.pipeline_component import PipelineComponent


class FilterByRegex(PipelineComponent):
    """Filter data elements with a filename matching a specified regex."""

    def __init__(self):
        super().__init__()
        self.applies_to_available = True
        self.configure()

    def __call__(self, dataset):

        to_trim = []
        for i in self.get_target_indexes(dataset):
            if re.match(self.pattern, str(dataset.files[i])):
                to_trim.append(i)
        dataset.files, trimmed = trim_list_by_inds(dataset.files, to_trim)
        dataset.filtered["regex"] = trimmed

        return trimmed

    def configure(self, pattern="/(?=a)b/"):
        """Configure the regex pattern to match (default does not filter).

        :param pattern: pattern to filter by
        :type pattern: str
        """
        self.pattern = pattern
