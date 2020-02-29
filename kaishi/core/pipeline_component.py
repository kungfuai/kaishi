"""Core filters for multiple dataset types."""
import warnings
import re
import numpy as np


class PipelineComponent:
    """Base class for pipeline components."""

    def __init__(self, dataset):
        self.dataset = dataset
        self.target_criteria = [".*"]

    def configure(self):
        warnings.warn("No options to configure for " + self.__class__.__name__)

    def applies_to(self, target_criteria):
        if not isinstance(target_criteria, list):
            self.target_criteria = [target_criteria]
        else:
            self.target_criteria = target_criteria

    def get_target_indexes(self):
        targets = []
        for i, fobj in enumerate(self.dataset.files):
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
        if isinstance(target, (int, np.int, np.int8, np.int16, np.int32, np.int64)):
            return True
        else:
            return False

    def _is_valid_target_str(self, target):
        if isinstance(target, str):
            return True
        else:
            return False
