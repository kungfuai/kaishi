"""Class definition for filtering duplicate rows in each dataframe."""
from kaishi.core.pipeline_component import PipelineComponent


class FilterDuplicateRowsEachDataframe(PipelineComponent):
    """Filter duplicate rows in each dataframe of a tabular dataset."""

    def __init__(self):
        """Initialize new filter component."""
        super().__init__()
        self.applies_to_available = True

    def __call__(self, dataset):
        """Perform the filter operation on a given tabular dataset.

        :param dataset: dataset to perform operation on
        :type dataset: :class:`kaishi.tabular.dataset.TabularDataset`
        """
        valid_indexes = dataset._get_indexes_with_valid_dataframe()
        targets = list(set(valid_indexes) & set(self.get_target_indexes(dataset)))
        for i in targets:
            dataset.files[i].df.drop_duplicates(inplace=True)
