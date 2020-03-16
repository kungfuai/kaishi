"""Filters for image datasets."""
import os
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.misc import find_similar_by_value
from kaishi.core.misc import CollapseChildren


class FilterSimilar(PipelineComponent):
    """Filter near duplicate files, detected via perceptual hashing ('imagehash' library)."""

    def __init__(self):
        super().__init__()
        self.configure()

    def __call__(self, dataset):
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

        return trimmed

    def configure(self, perceptual_hash_threshold=3):
        self.perceptual_hash_threshold = perceptual_hash_threshold
