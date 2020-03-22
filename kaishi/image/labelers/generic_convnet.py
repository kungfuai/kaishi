"""Class definition for generic convnet labeler."""
import numpy as np
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.image.model import Model


class LabelerGenericConvnet(PipelineComponent):
    """Use pre-trained ConvNet to predict image labels (e.g. stretched, rotated, etc.).

    This labeler uses a default configured :class:`kaishi.image.model.Model` object where the output layer is assumed
    to have 6 values ranging 0 to 1, where the labels are [DOCUMENT, RECTIFIED, ROTATED_RIGHT, ROTATED_LEFT,
    UPSIDE_DOWN, STRETCHED].
    """

    def __init__(self):
        """Initialize a new generic convnet labeler component."""
        super().__init__()

    def __call__(self, dataset):
        """Perform the labeling operation on an image dataset.

        :param dataset: kaishi image dataset
        :type dataset: :class:`kaishi.image.dataset.ImageDataset`
        """
        if dataset.model is None:
            dataset.model = Model()
        for batch, fobjs in dataset.build_numpy_batches(
            batch_size=dataset.model.batch_size
        ):
            pred = dataset.model.predict(batch)
            for i in range(len(fobjs)):
                if pred[i, 0] > 0.5:
                    fobjs[i].add_label("DOCUMENT")
                rot = np.argmax(pred[i, 1:5])
                if rot == 0:
                    fobjs[i].add_label("RECTIFIED")
                elif rot == 1:
                    fobjs[i].add_label("ROTATED_RIGHT")
                elif rot == 2:
                    fobjs[i].add_label("ROTATED_LEFT")
                else:
                    fobjs[i].add_label("UPSIDE_DOWN")
                if pred[i, 5] > 0.5:
                    fobjs[i].add_label("STRETCHED")
        dataset.labeled = True
