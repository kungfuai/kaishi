"""Basic class definition for a pipeline object."""

class Pipeline:
    """Base class for a generic pipeline object."""
    def __init__(self, methods=None, args=None):
        if methods is not None and args is not None:
            self.methods = methods
            self.args = args
        else:
            self.methods = []
            self.args = []

        return

    def run(self, verbose=False):
        """Run the full pipeline as configured."""
        for (pm, args) in zip(self.methods, self.args):
            if verbose:
                print('Running ' + pm.__name__)
            pm(*args)

        return

"""
class PipelineComponent:
    def __init__(self, func, args=[]):
        self.func = func
        self.args = args
        return

    def __call__(self, dataset_object):
"""
