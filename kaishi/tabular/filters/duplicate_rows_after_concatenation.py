"""Filters for image datasets."""
from kaishi.core.pipeline_component import PipelineComponent


class FilterDuplicateRowsAfterConcatenation(PipelineComponent):
    """Filter duplicate rows in each dataframe."""

    def __init__(self):
        super().__init__()

    def __call__(self, dataset):
        dataset.concatenate_all()
        dataset.df_concatenated.drop_duplicates(inplace=True)
