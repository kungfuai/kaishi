from kaishi.core.misc import (
    trim_list_by_inds,
    find_duplicate_inds,
    find_similar_by_value,
    md5sum,
)


def test_trim_list_by_inds():
    newlist, trimmed = trim_list_by_inds([2, 0, 3, 1], [3, 0, 2])
    assert len(newlist) == 1 and newlist[0] == 0
    assert len(trimmed) == 3 and 1 in trimmed and 2 in trimmed and 3 in trimmed


def test_find_duplicate_inds():
    badind, parentind = find_duplicate_inds([0, 1, 1, 2])
    assert len(badind) == 1 and len(parentind) == 1
    assert (badind[0] == 1 and parentind[0] == 2) or (
        badind[0] == 2 and parentind[0] == 1
    )


def test_find_similar_by_value():
    badind, parentind = find_similar_by_value([0, 4, 5, 9], 2)
    assert len(badind) == 1 and len(parentind) == 1
    assert (badind[0] == 1 and parentind[0] == 2) or (
        badind[0] == 2 and parentind[0] == 1
    )


def test_md5sum():
    hash_value = md5sum("tests/data/image/sample.jpg")
    assert hash_value == "df11f7053426c06d1c6073f88571ac40"
