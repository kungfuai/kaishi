"""Class definition for reading/writing files of various types."""
import os
from kaishi.util.misc import find_duplicate_inds
from kaishi.util.misc import trim_list_by_inds
from kaishi.util.misc import md5sum
from kaishi.util.misc import load_files_by_walk
import multiprocessing


class File:
    """Class that contains details about a file."""
    def __init__(self, basedir, relpath, filename):
        """Initialize basic file details."""
        self.relative_path = relpath
        self.children = {'duplicates': []}
        self.labels = []
        _ , self.ext = os.path.splitext(filename)
        self.basename = filename
        if relpath is not None:
            self.abspath = os.path.join(basedir, relpath, filename)
        else:
            self.abspath = os.path.join(basedir, filename)
        self.hash = None  # Default to None, populate later

        return

    def __repr__(self):
        if self.relative_path is None:
            return self.basename
        else:
            return os.path.join(self.relative_path, self.basename)

    def __str__(self):
        return self.__repr__()

    def compute_hash(self):
        """Compute the hash of the file."""
        self.hash = md5sum(self.abspath)

        return self.hash

    def add_label(self, label):
        """Add a label to a file object."""
        if label not in self.labels:
            self.labels.append(label)
        self.labels.sort()

        return

    def remove_label(self, label):
        """Remove a label from a file object."""
        try:
            self.labels.remove(label)
        except ValueError:
            return
        return

class FileGroup:
    """Class for readind and performing general operations on files."""

    def __init__(self):
        """Instantiate empty class."""
        self.files = []
        self.filtered = dict()

        return

    def load_dir(self, dir_name):
        """Read file names in a directory while ignoring subdirectories."""
        self.dir_name, self.dir_children, self.files = load_files_by_walk(dir_name, File)

        return

    def filter_duplicates(self):
        """Filter duplicate files, detected via hashing."""
        hashlist = [f.hash if f.hash is not None else f.compute_hash() for f in self.files]

        duplicate_ind, parent_ind = find_duplicate_inds(hashlist)
        for di, pi in zip(duplicate_ind, parent_ind):
            self.files[pi].children['duplicates'].append(self.files[di])
        self.files, trimmed = trim_list_by_inds(self.files, duplicate_ind)
        self.filtered['duplicates'] = trimmed

        return trimmed

    def show_available_filters(self):
        """Shows available member function filters."""
        for m in dir(self):
            if m.startswith('filter_'):
                print(m)

        return

    def collapse_children(self):
        """Restructure potentially multi-layer file tree into a single parent/child layer."""
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

        for f in self.files:  # Recursively collapse tree for all files in this group
            recursive_collapse_children(f, f.children)

        return

    def report(self):
        """Show a report of valid and invalid data."""
        if self.files == [] and self.filtered == {}:
            print('No data loaded to report on.')
            return

        print('Valid files:')
        for f in self.files:
            print('\t' + repr(f) + '\t' + repr(f.children))

        print('Invalid files:')
        for k in self.filtered.keys():
            print('\t%s:' % k)
            for f in self.filtered[k]:
                print('\t\t' + repr(f))

        return
