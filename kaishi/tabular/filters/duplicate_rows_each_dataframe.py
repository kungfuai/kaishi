"""Filters for image datasets."""
from kaishi.core.pipeline_component import PipelineComponent


class FilterDuplicateRowsEachDataframe(PipelineComponent):
    """Filter duplicate rows in each dataframe."""

    def __init__(self):
        super().__init__()
        self.applies_to_available = True

    def __call__(self, dataset):
        valid_indexes = dataset._get_indexes_with_valid_dataframe()
        targets = list(set(valid_indexes) & set(self.get_target_indexes(dataset)))
        for i in targets:
            dataset.files[i].df.drop_duplicates(inplace=True)
