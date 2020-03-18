"""Class definition for validation and test labeler."""
import random
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.pipeline_component import PipelineComponent


class LabelerValidationAndTest(PipelineComponent):
    """Assign validation and/or test data labels."""

    def __init__(self):
        super().__init__()
        self.configure()

    def __call__(self, dataset):
        val_ind = []
        test_ind = []
        if self.val_frac + self.test_frac > 1.0:
            raise ValueError("Validiation and test fractions must sum to < 1")
        all_ind = list(range(len(dataset.files)))

        if self.seed is not None:
            random.seed(self.seed)
        val_ind = random.sample(all_ind, round(len(dataset.files) * self.val_frac))
        remaining, _ = trim_list_by_inds(all_ind, val_ind)
        test_relative_ind = random.sample(
            list(range(len(remaining))), round(len(dataset.files) * self.test_frac)
        )
        test_ind = [remaining[i] for i in test_relative_ind]
        train_relative_ind, _ = trim_list_by_inds(
            list(range(len(remaining))), test_relative_ind
        )
        train_ind = [remaining[i] for i in train_relative_ind]

        for i in val_ind:
            dataset.files[i].add_label("VALIDATE")
        for i in test_ind:
            dataset.files[i].add_label("TEST")
        for i in train_ind:
            dataset.files[i].add_label("TRAIN")

    def configure(self, val_frac: float = 0.2, test_frac: float = 0.0, seed=None):
        """Configure the labeler (note: any nonlabeled data point is automatically assigned a "TRAIN" label).

        :param val_frac: fraction of data points to assign "VALIDATE" label
        :type val_frac: float
        :param test_frac: fraction of data points to assign "TEST" label
        :type test_frac: float
        :param seed: random seed for reproducibility
        :type seed: int
        """
        self.val_frac = val_frac
        self.test_frac = test_frac
        self.seed = seed
