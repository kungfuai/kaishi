"""Labelers for image datasets."""
import numpy as np
from kaishi.core.labels import Labels
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.image.model import Model


class LabelerGenericConvnet(PipelineComponent):
    """Use pre-trained ConvNet to predict image labels (e.g. stretched, rotated, etc.)."""

    def __init__(self):
        super().__init__()

    def __call__(self, dataset):
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
