"""Enumeration definition for labels."""
from enum import Enum


class Labels(Enum):
    """Enumeration of possible data labels."""

    RECTIFIED = 0
    ROTATED_RIGHT = 1
    ROTATED_LEFT = 2
    UPSIDE_DOWN = 3
    DOCUMENT = 4
    STRETCHED = 5
    GRAYSCALE = 6
    TRAIN = 7
    VALIDATE = 8
    TEST = 9
