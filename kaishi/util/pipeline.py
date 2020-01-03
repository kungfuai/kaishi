"""Basic class definition for a pipeline object."""

class Pipeline:
    """Base class for a generic pipeline object."""
    def __init__(self):
        self.components = []

        return

    def __call__(self, dataset, verbose=False):
        """Run the full pipeline as configured."""
        for component in self.components:
            if verbose:
                print('Running ' + component.__class__.__name__)
            component()

        return

    def __repr__(self):
        """Print pipeline overview."""
        if len(self.components) == 0:
            return 'Empty Kaishi pipeline'
        else:
            ret_str = 'Kaishi pipeline: '
            for i, component in enumerate(self.components):
                if component.__class__.__name__ == 'CollapseChildren':
                    ret_str += 'CollapseChildren (required)'
                else:
                    ret_str += component.__class__.__name__ + ' -> '

            return ret_str

    def __str__(self):
        return self.__repr__()

    def add_component(self, component):
        """Add a method to be called as a pipeline step, where the only argument to each will be the dataset object."""
        self.components.append(component)

        return

    def reset(self):
        """Reset the pipeline by removing all components."""
        self.components = []

        return
