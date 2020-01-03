import numpy as np
from kaishi.core.image.model import Model


class LabelerMacro():
    """Use pre-trained ConvNet to predict image labels (e.g. stretched, rotated, etc.)."""
    def __init__(self, dataset):
        self.dataset = dataset

        return

    def __call__(self):
        if self.dataset.model is None:
            self.dataset.model = Model()
        for batch, fobjs in self.dataset.build_numpy_batches(batch_size=self.dataset.model.batch_size):
            pred = self.dataset.model.predict(batch)
            for i in range(len(fobjs)):
                if pred[i, 0] > 0.5:
                    fobjs[i].add_label('DOCUMENT')
                rot = np.argmax(pred[i, 1:5])
                if rot == 0:
                    fobjs[i].add_label('RECTIFIED')
                elif rot == 1:
                    fobjs[i].add_label('ROTATED_RIGHT')
                elif rot == 2:
                    fobjs[i].add_label('ROTATED_LEFT')
                else:
                    fobjs[i].add_label('UPSIDE_DOWN')
                if pred[i, 5] > 0.5:
                    fobjs[i].add_label('STRETCHED')
        self.dataset.labeled = True

        return