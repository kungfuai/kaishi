"""Core filters for multiple dataset types."""
import warnings


class PipelineComponent:
    """Base class for pipeline components."""

    def __init__(self, dataset):
        self.dataset = dataset

    def configure(self):
        warnings.warn("No options to configure for " + self.__class__.__name__)
