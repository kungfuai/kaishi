"""Class definition for pipeline components."""
import warnings
import re
import numpy as np


class PipelineComponent:
    """Base class for pipeline components."""

    def __init__(self):
        self.applies_to_available = False
        self.target_criteria = [".*"]

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__

    def configure(self):
        """Method to configure via named arguments. Defaults to no configurations, unless inherited and overridden."""
        warnings.warn("No options to configure for " + self.__class__.__name__)

    def applies_to(self, target_criteria):
        """Limit data files that the component applies to via regex.

        :param target_criteria: list or string containing a regex to denote files that this component applies to
        """
        if not self.applies_to_available:
            raise NotImplementedError(
                "applies_to() method not implemented for " + self.__class__.__name__
            )
        if not isinstance(target_criteria, list):
            self.target_criteria = [target_criteria]
        else:
            self.target_criteria = target_criteria

    def get_target_indexes(self, dataset):
        """Get target indexes of a dataset based on criteria set using the `applies_to()` method

        :param dataset: dataset to inspect
        :type dataset: initialized kaishi dataset object (e.g. :class:`kaishi.core.dataset.FileDatset`)
        :return: list of indexes
        :rtype: list of int
        """
        targets = []
        for i, fobj in enumerate(dataset.files):
            for criterion in self.target_criteria:
                if self._is_valid_target_int(criterion):
                    if i == criterion:
                        targets.append(i)
                elif self._is_valid_target_str(criterion):
                    if re.match(criterion, str(fobj)):
                        targets.append(i)
                else:
                    raise TypeError(
                        "Unrecognized type for 'applies_to()' target criteria"
                    )
        return targets

    def _is_valid_target_int(self, target):
        """Check if an index is a valid integer type.

        :param target: target to verify
        :type target: int (or similar, e.g. np.int32)
        :return: flag indicating if the target is a valid integer type
        :rtype: bool
        """
        if isinstance(target, (int, np.int, np.int8, np.int16, np.int32, np.int64)):
            return True
        else:
            return False

    def _is_valid_target_str(self, target):
        """Check if an index is a valid string type.

        :param target: target to verify
        :type target: int (or similar)
        :return: flag indicating if the target is a valid string type
        :rtype: bool
        """
        if isinstance(target, str):
            return True
        else:
            return False
