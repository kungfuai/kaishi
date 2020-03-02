"""Filters for image datasets."""
from kaishi.core.pipeline_component import PipelineComponent


class FilterDuplicateRowsEachDataframe(PipelineComponent):
    """Filter duplicate rows in each dataframe."""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.applies_to_available = True

    def __call__(self):
        valid_indexes = self.dataset.get_indexes_with_valid_dataframe()
        targets = list(set(valid_indexes) & set(self.get_target_indexes()))
        for i in targets:
            self.dataset.files[i].df.drop_duplicates(inplace=True)
