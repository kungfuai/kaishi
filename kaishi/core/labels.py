"""Enumerations for labels."""
from enum import Enum


class Labels(Enum):
    """All fields."""

    RECTIFIED = 0
    ROTATED_RIGHT = 1
    ROTATED_LEFT = 2
    UPSIDE_DOWN = 3
    DOCUMENT = 4
    STRETCHED = 5
