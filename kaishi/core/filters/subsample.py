"""Core filters for multiple dataset types."""
import re
import random
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.pipeline_component import PipelineComponent


class FilterSubsample(PipelineComponent):
    """Filter duplicate files, detected via hashing."""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.configure()

    def __call__(self):

        if self.N is None or len(self.dataset.files) <= self.N:
            return []
        all_inds = list(range(len(self.dataset.files)))
        if self.seed is not None:
            random.seed(self.seed)
        to_trim = random.sample(all_inds, len(self.dataset.files) - self.N)
        self.dataset.files, trimmed = trim_list_by_inds(self.dataset.files, to_trim)
        self.dataset.filtered["subsample"] = trimmed

        return trimmed

    def configure(self, N=None, seed=None):
        """Default configuration returns false always."""
        self.N = N
        self.seed = seed
