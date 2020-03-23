"""Definitions for print helper utilities."""


def should_print_row(i: int, max_entries: int, num_entries: int):
    """Make decision to print row or not based on max_rows.

    :param i: index of row
    :type i: int
    :param max_entries: max number of entries for the table
    :type max_entries: int
    :param num_entries: number of possible entries (the full list)
    :type num_entries: int
    :return: 0 if should not print, 1 if should print, 2 if should print ellipsis ("...")
    :rtype: int
    """
    if num_entries <= max_entries:
        return 1
    else:
        gap_i_lower = max_entries // 2
        gap_i_upper = num_entries - (max_entries - gap_i_lower)
        if i == gap_i_lower:
            # Ellipsis line
            return 2
        elif i <= gap_i_lower or i >= gap_i_upper:
            # Print data
            return 1
        else:
            # Do not print
            return 0
