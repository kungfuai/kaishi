"""Class definition for filter by label."""
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.pipeline_component import PipelineComponent


class FilterByLabel(PipelineComponent):
    """Filter each element of a dataset by a specified label."""

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
        """Specify the label to filter.

        :param label_to_filter: data elements with this label will be filtered
        :type label_to_filter: str
        """
        self.label_to_filter = label_to_filter
