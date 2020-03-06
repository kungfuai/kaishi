"""Transform image(s) to grayscale."""
from kaishi.core.pipeline_component import PipelineComponent


class TransformToGrayscale(PipelineComponent):
    """Filter file list if non-image extensions exist."""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.applies_to_available = True

    def __call__(self):
        # Trim any files without image extensions
        for i in self.get_target_indexes():
            self.dataset.files[i].convert_to_grayscale()
