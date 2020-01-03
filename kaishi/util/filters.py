from kaishi.util.misc import find_duplicate_inds
from kaishi.util.misc import trim_list_by_inds


class FilterDuplicates():
    """Filter duplicate files, detected via hashing."""
    def __init__(self, dataset):
        self.dataset = dataset

        return

    def __call__(self):
        hashlist = [f.hash if f.hash is not None else f.compute_hash() for f in self.dataset.files]

        duplicate_ind, parent_ind = find_duplicate_inds(hashlist)
        for di, pi in zip(duplicate_ind, parent_ind):
            self.dataset.files[pi].children['duplicates'].append(self.dataset.files[di])
        self.dataset.files, trimmed = trim_list_by_inds(self.dataset.files, duplicate_ind)
        self.dataset.filtered['duplicates'] = trimmed

        return trimmed
