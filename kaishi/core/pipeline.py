"""Basic class definition for a pipeline object."""
import inspect


class Pipeline:
    """Base class for a generic pipeline object."""

    def __init__(self):
        self.components = []
        self.completed_steps = []

    def __call__(self, dataset, verbose: bool = False):
        """Run the full pipeline as configured."""
        for component in self.components:
            if verbose:
                print("Running " + component.__class__.__name__)
            component(dataset)
            self.completed_steps.append(
                {
                    "step": component.__class__.__name__,
                    "config": self._get_configs_for_component(component),
                }
            )

    def __repr__(self):
        """Print pipeline overview."""
        if len(self.components) == 0:
            return "Empty Kaishi pipeline"
        ret_str = "Kaishi pipeline: \n"
        for i, component in enumerate(self.components):
            ret_str += repr(i) + ": " + component.__class__.__name__ + "\n"
            args = self._get_configs_for_component(component)
            if len(args) == 0:
                continue
            else:
                for arg in args:
                    ret_str += "     " + arg + ": " + repr(args[arg]) + "\n"

        return ret_str

    def __str__(self):
        return self.__repr__()

    def _get_configs_for_component(self, initialized_component):
        """Get args and values of them from an initialized component."""
        args = dict()
        for arg in inspect.getfullargspec(initialized_component.configure).args:
            if arg == "self":
                continue
            args[arg] = getattr(initialized_component, arg)

        return args

    def add_component(self, component):
        """Add a method to be called as a pipeline step, where the only arg is a dataset object."""
        self.components.append(component)

    def remove_component(self, index):
        """Remove a pipeline method by index."""
        self.components.pop(index)

    def reset(self):
        """Reset the pipeline by removing all components."""
        self.components = []
