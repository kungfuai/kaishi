import os
from kaishi.util.misc import trim_list_by_inds
from kaishi.util.misc import find_similar_by_value


def filter_similar(self, threshold):
    """Filter near duplicate files, detected via perceptual hashing ('imagehash' library)."""
    hashlist = [f.perceptual_hash if f.perceptual_hash is not None else f.compute_perceptual_hash() for f in self.files]

    duplicate_ind, parent_ind = find_similar_by_value(hashlist, threshold)
    for di, pi in zip(duplicate_ind, parent_ind):
        self.files[pi].children['similar'].append(self.files[di])
    self.files, trimmed = trim_list_by_inds(self.files, duplicate_ind)
    self.filtered['similar'] = trimmed

    return trimmed

def filter_invalid_file_extensions(self):
    """Filter file list if non-image extensions exist."""

    # Trim any files without image extensions
    badind = []
    for i, f in enumerate(self.files):
        _, ext = os.path.splitext(f.basename)
        if len(ext) == 0 or ext not in self.VALID_EXT:
            badind.append(i)

    self.files, trimmed = trim_list_by_inds(self.files, badind)
    self.filtered['unsupported_extension'] = trimmed

    return trimmed

def filter_invalid_image_headers(self):
    """Filter file list if image files have invalid or nonexistent header."""

    badind = []
    for i, f in enumerate(self.files):
        if not self.validate_image_header(f.abspath):
            badind.append(i)

    self.files, trimmed = trim_list_by_inds(self.files, badind)
    self.filtered['invalid_header'] = trimmed

    return trimmed
