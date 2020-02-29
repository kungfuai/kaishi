"""Filters for image datasets."""
import os
from kaishi.core.pipeline_component import PipelineComponent


class FilterDuplicateRowsAfterConcatenation(PipelineComponent):
    """Filter duplicate rows in each dataframe."""

    def __init__(self, dataset):
        super().__init__(dataset)

    def __call__(self):
        self.dataset.concatenate_all()
        self.dataset.df_concatenated.drop_duplicates(inplace=True)
