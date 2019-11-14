"""Class definition for reading/writing files of various types."""
import os
from kaishi.util.misc import find_duplicate_inds
from kaishi.util.misc import trim_list_by_inds
from kaishi.util.misc import md5sum
from kaishi.util.misc import load_files_by_walk


class File:
    """Class that contains details about a file."""
    def __init__(self, basedir, relpath, filename):
        """Initialize basic file details."""
        self.relative_path = relpath
        _ , self.ext = os.path.splitext(filename)
        self.basename = filename
        if relpath is not None:
            self.abspath = os.path.join(basedir, relpath, filename)
        else:
            self.abspath = os.path.join(basedir, filename)
        self.hash = None  # Default to None, populate later
        
        return

    def compute_hash(self):
        """Compute the hash of the file."""
        self.hash = md5sum(self.abspath)

        return self.hash

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

        duplicate_ind = find_duplicate_inds(hashlist)
        self.files, trimmed = trim_list_by_inds(self.files, duplicate_ind)
        self.filtered['duplicates'] = trimmed

        return trimmed

    def show_available_filters(self):
        """Shows available member function filters."""
        for m in dir(self):
            if m.startswith('filter_'):
                print(m)

        return

    def report(self):
        """Show a report of valid and invalid data."""
        if self.files == [] and self.filtered == {}:
            print('No data loaded to report on.')
            return

        print('Valid files:')
        for f in self.files:
            print('\t%s' % f.basename)

        print('Invalid files:')
        for k in self.filtered.keys():
            print('\t%s:' % k)
            for f in self.filtered[k]:
                print('\t\t%s' % f.basename)

        return
