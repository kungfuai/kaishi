"""Class definition for subsampling filter."""
import random
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.pipeline_component import PipelineComponent


class FilterSubsample(PipelineComponent):
    """Filter by subsampling."""

    def __init__(self):
        super().__init__()
        self.configure()

    def __call__(self, dataset):

        if self.N is None or len(dataset.files) <= self.N:
            return []
        all_inds = list(range(len(dataset.files)))
        if self.seed is not None:
            random.seed(self.seed)
        to_trim = random.sample(all_inds, len(dataset.files) - self.N)
        dataset.files, trimmed = trim_list_by_inds(dataset.files, to_trim)
        dataset.filtered["subsample"] = trimmed

        return trimmed

    def configure(self, N=None, seed=None):
        """Configuration options for subsample filter.

        :param N: number of data points to keep
        :type N: int
        :param seed: random seed for reproducibility
        :type seed: int
        """
        self.N = N
        self.seed = seed
