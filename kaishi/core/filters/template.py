"""Core filters for multiple dataset types."""
from kaishi.core.pipeline_component import PipelineComponent


class TemplateForFilter(PipelineComponent):
    """Template for creating custom filters"""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.configure()

    def __call__(self):
        # Perform all modifications to the dataset here, typically by making observations
        # of the `self.files` list, filtering elements, and then adding to the
        # `self.filtered` dictionary (the key is the reason for filtering, e.g. "duplicate")
        self.filtered["duplicate"].append(self.files.pop[0])

    def configure(self, arg1=1234567890, arg2=False):
        """Default configuration."""
        self.arg1 = arg1
        self.arg2 = arg2
        # ... etc.
