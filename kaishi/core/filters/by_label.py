"""Core filters for multiple dataset types."""
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.pipeline_component import PipelineComponent


class FilterByLabel(PipelineComponent):
    """Filter by a label string."""

    def __init__(self):
        super().__init__()
        self.applies_to_available = True
        self.configure()

    def __call__(self, dataset):

        if self.label_to_filter is None:
            return []
        to_trim = []
        for i in self.get_target_indexes(dataset):
            if dataset.files[i].has_label(self.label_to_filter):
                to_trim.append(i)
        dataset.files, trimmed = trim_list_by_inds(dataset.files, to_trim)
        dataset.filtered["label_match"] = trimmed

        return trimmed

    def configure(self, label_to_filter=None):
        """Default configuration returns false always."""
        self.label_to_filter = label_to_filter
