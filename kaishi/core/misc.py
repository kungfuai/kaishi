"""Miscellaneous helper functions."""
import hashlib
import os
import numpy as np
from kaishi.core.pipeline_component import PipelineComponent


def load_files_by_walk(dir_name_raw: str, file_initializer, recursive: bool = False):
    """Load files from a directory with an option to recurse.

    :param dir_name_raw: Directory to load file structure from
    :type dir_name_raw: str
    :param file_initializer: Data file class to initialize each file with
    :type file_initializer: kaishi file initializer class (e.g. :class:`kaishi.core.file.File`)
    :param recursive: Option to load recursively, defaults to False
    :type recursive: bool
    :return: canonical directory name, list of subdirectories, and list of initialized files
    :rtype: str, list, and list
    """
    dir_name = os.path.abspath(dir_name_raw)
    dir_children = []
    files = []
    for root, _, filenames in os.walk(dir_name):
        relative_path = None  # Assume we're in the 'dir_name' directory before checking
        if os.path.abspath(root) != os.path.abspath(dir_name):
            if recursive is False:
                continue
            relative_path = os.path.abspath(root)[len(dir_name) + 1 :]
            if relative_path not in dir_children:
                dir_children.append(relative_path)
        for filename in filenames:
            files.append(file_initializer(dir_name, relative_path, filename))

    return dir_name, dir_children, files


def trim_list_by_inds(list_to_trim: list, indices: list):
    """Trim a list given an unordered list of indices.

    :param list_to_trim: list to remove elements from
    :type list_to_trim: list
    :param indices: indices of list items to remove
    :type indices: list
    :return: new list, trimmed items
    :rtype: list, list
    """

    new_list = list_to_trim.copy()
    trimmed = []

    for index in sorted(indices, reverse=True):
        trimmed.append(new_list[index])
        del new_list[index]

    return new_list, trimmed


def find_duplicate_inds(list_with_duplicates: list):
    """Find indices of duplicates in a list.

    :param list_with_duplicates: list containing duplicate items
    :type list_with_duplicates: list
    :return: list of duplicate indices, list of unique items (parents of duplicates)
    :rtype: list and list
    """
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


def find_similar_by_value(list_of_values: list, difference_threshold):
    """Find near duplicates based on similar reference value.

    :param list_of_values: list of values to compare
    :type list_of_values: list
    :param difference_threshold: differences above this threshold will be identified for removal
    :return: list of similar indices, list of unique items (parents of similar items)
    :rtype: list and list
    """

    badind = []
    parentind = []
    if not isinstance(
        list_of_values, np.ndarray
    ):  # Make sure it's a numpy array, convert if not
        array_of_values = np.array(list_of_values)
    else:
        array_of_values = list_of_values

    for i in range(len(array_of_values) - 1, -1, -1):
        if array_of_values[i] is None:
            array_of_values = array_of_values[:-1]
            continue
        differences = np.array(
            [
                difference_threshold + 1
                if value is None
                else np.abs(value - array_of_values[-1])
                for value in array_of_values[:-1]
            ]
        )
        found_locs = np.nonzero(differences <= difference_threshold)[0]

        if len(found_locs) > 0:
            badind.append(i)
            parentind.append(found_locs[0])
        array_of_values = array_of_values[:-1]

    return badind, parentind


def md5sum(filename: str):
    """Compute the md5sum of a file.

    :param filename: name of file to compute hash of
    :type filename: str
    :return: hash value
    """
    with open(filename, "rb") as fd:
        buf = fd.read()
        hasher = hashlib.md5()
        hasher.update(buf)

        return hasher.hexdigest()


class CollapseChildren(PipelineComponent):
    """Restructure potentially multi-layer file tree into a single parent/child layer."""

    def __init__(self):
        super().__init__()

    def __call__(self, dataset):
        def recursive_collapse_children(
            parent, top_level_children, top_level_call=True, top_level_key=None
        ):
            for k in parent.children:
                if top_level_call:
                    top_level_key = k
                if len(parent.children[k]) == 0:
                    continue
                for child in parent.children[k]:
                    recursive_collapse_children(
                        child, top_level_children, False, top_level_key
                    )
                    if not top_level_call:
                        top_level_children[top_level_key].append(child)
            if not top_level_call:
                for k in parent.children:
                    parent.children[k] = []

        for (
            fobj
        ) in dataset.files:  # Recursively collapse tree for all files in this group
            recursive_collapse_children(fobj, fobj.children)


def is_valid_label(label_str: str, label_enum):
    """Check if a label is contained in an  enum.

    :param label_str: string defining the label
    :type label_str: str
    :return: flag indicating if label is valid
    :rtype: bool
    """
    return bool(label_str in [label.name for label in label_enum])
