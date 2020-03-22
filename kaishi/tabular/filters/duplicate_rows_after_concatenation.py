"""Class definition for filtering duplicate rows after concatenation."""
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.tabular.aggregators.concatenate_dataframes import (
    AggregatorConcatenateDataframes,
)


class FilterDuplicateRowsAfterConcatenation(PipelineComponent):
    """Filter duplicate rows in the concatenated dataframe (dataset will be concatenated if it hasn't been already)."""

    def __init__(self):
        """Initialize new filter object."""
        super().__init__()
        self.applies_to_available = True

    def __call__(self, dataset):
        """Perform filter on a given tabular dataset.

        :param dataset: tabular dataset to perform operation on
        :type dataset: :class:`kaishi.tabular.dataset.TabularDataset`
        """
        concatenator = AggregatorConcatenateDataframes()
        concatenator.applies_to(self.target_criteria)
        concatenator(dataset)
        dataset.artifacts["df_concatenated"].drop_duplicates(inplace=True)
