"""Miscellaneous helper functions."""
import hashlib


def trim_list_by_inds(list_to_trim, indices):
    """Trim a list given an unordered list of indices."""
    new_list = list_to_trim.copy()

    for index in sorted(indices, reverse=True):
        del new_list[index]

    return new_list

def md5sum(filename):
    """Compute the md5sum of a file."""
    try:
        with open(filename, 'rb') as fd:
            buf = fd.read()
            hasher = hashlib.md5()
            hasher.update(buf)

            return hasher.hexdigest()

    except IsADirectoryError:
        return None
