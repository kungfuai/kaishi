"""Class definition for concatenating tabular data files."""
from kaishi.core.pipeline_component import PipelineComponent
import pandas as pd


class AggregatorConcatenateDataframes(PipelineComponent):
    """Concatenate all data frames."""

    def __init__(self):
        """Initialize new filter object."""
        super().__init__()
        self.applies_to_available = True

    def __call__(self, dataset):
        """Perform concatenation on a given dataset (all files must have the same schema).

        :param dataset: tabular dataset to perform operation on
        :type dataset: :class:`kaishi.tabular.dataset.TabularDataset`
        """
        i_with_valid_dataframes = dataset._get_indexes_with_valid_dataframe()
        i_valid_targets = self.get_target_indexes(dataset)
        i_intersection = list(set(i_with_valid_dataframes) & set(i_valid_targets))
        valid_dataframes = [dataset.files[i].df for i in i_intersection]

        dataset.artifacts["df_concatenated"] = pd.concat(valid_dataframes).reset_index(
            drop=True
        )
