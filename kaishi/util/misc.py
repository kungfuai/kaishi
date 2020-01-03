"""Miscellaneous helper functions."""
import hashlib
import numpy as np
import os


def load_files_by_walk(dir_name_raw, FileInitializer):
    """Read file names in a directory while ignoring subdirectories."""
    dir_name = os.path.abspath(dir_name_raw)
    dir_children = []
    files = []
    for root, dirs, filenames in os.walk(dir_name):
        relative_path = None  # Assume we're in the 'dir_name' directory before checking
        if len(os.path.abspath(root)) > len(dir_name):
            relative_path = os.path.abspath(root)[len(dir_name) + 1:]
            if relative_path not in dir_children:
                dir_children.append(relative_path)
        for filename in filenames:
            files.append(FileInitializer(dir_name, relative_path, filename))

    return dir_name, dir_children, files

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
    found = []
    foundind = []
    badind = []
    parentind = []

    for i, item in enumerate(list_with_duplicates):
        try:
            parentind.append(foundind[found.index(item)])
            badind.append(i)
        except ValueError:
            found.append(item)
            foundind.append(i)

    return badind, parentind

def find_similar_by_value(list_of_values, difference_threshold):
    """Find near duplicates based on similar reference value."""
    badind = []
    parentind = []
    if not isinstance(list_of_values, np.ndarray):  # Make sure it's a numpy array, convert if not
        array_of_values = np.array(list_of_values)
    else:
        array_of_values = list_of_values

    for i in range(len(array_of_values) - 1, -1, -1):  # Loop backwards so we can remove values as we go
        found_locs = np.nonzero((array_of_values[:-1] - array_of_values[-1]) <= difference_threshold)[0]

        if len(found_locs) > 0:
            badind.append(i)
            parentind.append(found_locs[0])
        array_of_values = array_of_values[:-1]

    return badind, parentind

def md5sum(filename):
    """Compute the md5sum of a file."""
    with open(filename, 'rb') as fd:
        buf = fd.read()
        hasher = hashlib.md5()
        hasher.update(buf)

        return hasher.hexdigest()

class CollapseChildren():
    """Restructure potentially multi-layer file tree into a single parent/child layer."""
    def __init__(self, dataset):
        self.dataset = dataset

        return

    def __call__(self):
        def recursive_collapse_children(parent, top_level_children, top_level_call=True, top_level_key=None):
            for k in parent.children.keys():
                if top_level_call:
                    top_level_key = k
                if len(parent.children[k]) == 0:
                    continue
                else:
                    for child in parent.children[k]:
                        recursive_collapse_children(child, top_level_children, False, top_level_key)
                        if not top_level_call:
                            top_level_children[top_level_key].append(child)
            if not top_level_call:
                for k in parent.children.keys():
                    parent.children[k] = []
            return

        for f in self.dataset.files:  # Recursively collapse tree for all files in this group
            recursive_collapse_children(f, f.children)

        return
