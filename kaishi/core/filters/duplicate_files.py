"""Class definition for filtering duplicate files."""
from kaishi.core.misc import find_duplicate_inds
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.misc import CollapseChildren
from kaishi.core.pipeline_component import PipelineComponent


class FilterDuplicateFiles(PipelineComponent):
    """Filter duplicate files, detected via hashing."""

    def __init__(self):
        super().__init__()

    def __call__(self, dataset):
        hashlist = [
            f.hash if f.hash is not None else f.compute_hash() for f in dataset.files
        ]

        duplicate_ind, parent_ind = find_duplicate_inds(hashlist)
        for di, pi in zip(duplicate_ind, parent_ind):
            dataset.files[pi].children["duplicates"].append(dataset.files[di])
        dataset.files, trimmed = trim_list_by_inds(dataset.files, duplicate_ind)
        dataset.filtered["duplicates"] = trimmed
        CollapseChildren()(dataset)

        return trimmed
