# Pipeline Components
Pipeline components are broken up into several distinct categories, and the classes that define them MUST begin with the correct keyword:
* `Filter*` - removes elements of a dataset
* `Transform*` - changes one or more data objects in some fundamental way
* `Labeler*` - creates labels for data objects without modifying the underlying data
* `Aggregator*` - combines data objects in some way

Look at how other pipeline components are implemented. Feel free to write your own, while following the below rules:
* Inherits from the `PipelineComponent` class
* Has no initialization arguments
* Has a single `__call__` method with a single argument (a dataset object)
* If specific configuration is needed, a method named `self.configure(...)` must be written with named arguments with defaults. `self.configure()` must be called as part of the `__init__(...)` call for configuration to work.
* `self.applies_to_available = True` must be in the `__init__(...)` call if the component takes advantage of the `self.applies_to()` and `self.get_target_indexes()` methods from `kaishi.core.pipeline_component.PipelineComponent` method
* If an artifact (i.e. some result) is created from the operation, as in the case of Aggregators, the artifact should be added to the `dataset.artifacts` dictionary (automatically initialized with any new dataset)

You can then enable usage of the component with your instantiated dataset object, e.g.:
```
from your_definition import YourNewComponent
imd.YourNewComponent = YourNewComponent
imd.configure_pipeline(['YourNewComponent'])
```
