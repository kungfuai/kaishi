"""Core module for Kaishi datasets.

This module contains classes, functions, etc. that are useful elsewhere in the project, as well as dataset definitions that are agnostic to the data type. In particular, the :class:`kaishi.core.dataset.FileDataset` class can be used to operate on any directory of files, regardless of the dataset. Specific data type modules (e.g. :any:`kaishi.image`) also inherit functionality from the core module.
"""
