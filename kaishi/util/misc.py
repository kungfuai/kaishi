"""Miscellaneous helper functions."""
import hashlib


def trim_list_by_inds(list_to_trim, indices):
    """Trim a list given an unordered list of indices."""
    new_list = list_to_trim.copy()
    trimmed = []

    for index in sorted(indices, reverse=True):
        trimmed.append(new_list[index])
        del new_list[index]

    return new_list, trimmed

def find_duplicate_inds(list_with_duplicates):
    """Find indices of duplicates in a list."""
    found = set([])
    badind = []
    
    for i, item in enumerate(list_with_duplicates):
        if item not in found:
            found.add(item)
        else:
            badind.append(i)

    return badind

def md5sum(filename):
    """Compute the md5sum of a file."""
    with open(filename, 'rb') as fd:
        buf = fd.read()
        hasher = hashlib.md5()
        hasher.update(buf)

        return hasher.hexdigest()
