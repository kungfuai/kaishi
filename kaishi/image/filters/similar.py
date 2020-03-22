"""Class definition for filtering similar images in a dataset."""
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.misc import find_similar_by_value
from kaishi.core.misc import CollapseChildren


class FilterSimilar(PipelineComponent):
    """Filter near duplicate files, detected via perceptual hashing (using the `imagehash` library)."""

    def __init__(self):
        """Initialize filter object."""
        super().__init__()
        self.configure()

    def __call__(self, dataset):
        """Perform filter operation on a specified dataset.

        :param dataset: dataset to perform operation on
        :type dataset: :class:`kaishi.image.dataset.ImageDataset`
        """
        hashlist = [
            f.perceptual_hash
            if f.perceptual_hash is not None
            else f.compute_perceptual_hash()
            for f in dataset.files
        ]

        duplicate_ind, parent_ind = find_similar_by_value(
            hashlist, self.perceptual_hash_threshold
        )
        for di, pi in zip(duplicate_ind, parent_ind):
            dataset.files[pi].children["similar"].append(dataset.files[di])
        dataset.files, trimmed = trim_list_by_inds(dataset.files, duplicate_ind)
        dataset.filtered["similar"] = trimmed
        CollapseChildren()(dataset)

    def configure(self, perceptual_hash_threshold=3):
        """Configure the filter with a perceptual hash threshold.

        :param perceptual_hash_threshold: threshold for determining whether or not images are similar (> are deemed not similar)
        :type perceptual_hash_threshold: int or float
        """
        self.perceptual_hash_threshold = perceptual_hash_threshold
