"""Core filters for multiple dataset types."""
import random
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.pipeline_component import PipelineComponent


class LabelerValidationAndTest(PipelineComponent):
    """Assign validation and/or test data"""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.configure()

    def __call__(self):

        val_ind = []
        test_ind = []
        if self.val_frac + self.test_frac > 1.0:
            raise ValueError("Validiation and test fractions must sum to < 1")
        all_ind = list(range(len(self.dataset.files)))

        if self.seed is not None:
            random.seed(self.seed)
        val_ind = random.sample(all_ind, round(len(self.dataset.files) * self.val_frac))
        _, remaining = trim_list_by_inds(all_ind, val_ind)
        test_ind = random.sample(
            remaining, round(len(self.dataset.files) * self.test_frac)
        )

        for i in val_ind:
            self.dataset.files[i].add_label("VALIDATE")
        for i in test_ind:
            self.dataset.files[i].add_label("TEST")

    def configure(self, val_frac=0.2, test_frac=0.0, seed=None):
        """Default configuration returns false always."""
        self.val_frac = val_frac
        self.test_frac = test_frac
        self.seed = seed
