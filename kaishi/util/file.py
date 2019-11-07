"""Class definition for reading/writing files of various types."""
import os
from kaishi.util.misc import find_duplicate_inds, trim_list_by_inds, md5sum 


class FileGroup:
    """Class for reading, writing, and performing general operations on files."""

    def __init__(self):
        """Instantiate empty class."""
        self.file = []
        self.filtered = dict()

        return

    def load_dir(self, dir_name):
        """Read file names in a directory while ignoring subdirectories."""
        self.dir_name = os.path.abspath(dir_name)
        self.files = [self.dir_name + '/' + bn for bn in os.listdir(dir_name)]

        badind = []
        for i, fn in enumerate(self.files):
            if os.path.isdir(fn):
                badind.append(i)

        self.files, _ = trim_list_by_inds(self.files, badind)

        return

    def filter_duplicates(self):
        """Filter duplicate files, detected via hashing."""
        hashlist = [md5sum(f) for f in self.files]

        duplicate_ind = find_duplicate_inds(hashlist)
        self.files, trimmed = trim_list_by_inds(self.files, duplicate_ind)
        self.filtered['duplicates'] = trimmed

        return

    def show_available_filters(self):
        """Shows available member function filters."""
        for m in dir(self):
            if m.startswith('filter_'):
                print(m)

        return

    def report(self):
        """Show a report of valid and invalid data."""
        print('Valid files:')
        for fn in self.files:
            print('\t%s' % os.path.basename(fn))

        print('Invalid files:')
        for k in self.filtered.keys():
            print('\t%s:' % k)
            for fn in self.filtered[k]:
                print('\t\t%s' % os.path.basename(fn))

        return
