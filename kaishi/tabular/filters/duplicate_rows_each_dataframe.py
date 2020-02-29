"""Filters for image datasets."""
from kaishi.core.pipeline_component import PipelineComponent


class FilterDuplicateRowsEachDataframe(PipelineComponent):
    """Filter duplicate rows in each dataframe."""

    def __init__(self, dataset):
        super().__init__(dataset)

    def __call__(self):
        for df in self.dataset.get_valid_dataframes():
            df.drop_duplicates(inplace=True)
