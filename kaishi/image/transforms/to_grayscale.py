"""Transform image(s) to grayscale."""
from kaishi.core.pipeline_component import PipelineComponent


class TransformToGrayscale(PipelineComponent):
    """Filter file list if non-image extensions exist."""

    def __init__(self):
        super().__init__()
        self.applies_to_available = True

    def __call__(self, dataset):
        # Trim any files without image extensions
        for i in self.get_target_indexes(dataset):
            dataset.files[i].convert_to_grayscale()
