"""Miscellaneous helper functions."""


def trim_list_by_inds(list_to_trim, indices):
    """Trim a list given an unordered list of indices."""
    new_list = list_to_trim.copy()

    for index in sorted(indices, reverse=True):
        del new_list[index]

    return new_list
