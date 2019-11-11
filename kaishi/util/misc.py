"""Miscellaneous helper functions."""
import hashlib
import numpy as np


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

def find_near_duplicates_by_value(list_of_values, difference_threshold):
    """Find near duplicates based on similar reference value."""
    badind = []
    if not isinstance(list_of_values, np.ndarray):  # Make sure it's a numpy array, convert if not
        array_of_values = np.array(list_of_values)
    else:
        array_of_values = list_of_values

    for i in range(len(array_of_values) - 1, -1, -1):  # Loop backwards so we can remove values as we go
        if np.any(np.abs(array_of_values[:-1] - array_of_values[-1]) <= difference_threshold):
            badind.append(i)
        array_of_values = array_of_values[:-1]

    return badind

def md5sum(filename):
    """Compute the md5sum of a file."""
    with open(filename, 'rb') as fd:
        buf = fd.read()
        hasher = hashlib.md5()
        hasher.update(buf)

        return hasher.hexdigest()
