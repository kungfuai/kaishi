"""Basic class definition for a pipeline object."""


class Pipeline:
    """Base class for a generic pipeline object."""

    def __init__(self):
        self.components = []

    def __call__(self, dataset, verbose: bool = False):
        """Run the full pipeline as configured."""
        for component in self.components:
            if verbose:
                print("Running " + component.__class__.__name__)
            component()

    def __repr__(self):
        """Print pipeline overview."""
        if len(self.components) == 0:
            return "Empty Kaishi pipeline"
        ret_str = "Kaishi pipeline: "
        for component in self.components:
            if component.__class__.__name__ == "CollapseChildren":
                ret_str += "CollapseChildren (required)"
            else:
                ret_str += component.__class__.__name__ + " -> "

        return ret_str

    def __str__(self):
        return self.__repr__()

    def add_component(self, component):
        """Add a method to be called as a pipeline step, where the only arg is a dataset object."""
        self.components.append(component)

    def remove_component(self, index):
        """Remove a pipeline method by index."""
        self.components.pop(index)

    def reset(self):
        """Reset the pipeline by removing all components."""
        self.components = []
