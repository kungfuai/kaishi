"""Class definition for reading/writing files of various types."""
import os
from kaishi.util.misc import find_duplicate_inds, trim_list_by_inds, md5sum 


class File:
    """Class that contains details about a file."""
    def __init__(self, filename):
        """Initialize basic file details."""
        self.dirname = os.path.dirname(filename)
        _ , self.ext = os.path.splitext(filename)
        self.basename = os.path.basename(filename)
        self.abspath = os.path.abspath(filename)
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
        self.dir_name = os.path.abspath(dir_name)
        self.files = [File(self.dir_name + '/' + bn) for bn in os.listdir(dir_name)]

        badind = []
        for i, f in enumerate(self.files):
            if os.path.isdir(f.abspath):
                badind.append(i)

        self.files, _ = trim_list_by_inds(self.files, badind)

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
        print('Valid files:')
        for f in self.files:
            print('\t%s' % f.basename)

        print('Invalid files:')
        for k in self.filtered.keys():
            print('\t%s:' % k)
            for f in self.filtered[k]:
                print('\t\t%s' % f.basename)

        return
