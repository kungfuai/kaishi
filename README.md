# kaishi
Tool kit to accelerate the initial phases of exploratory data analysis.

# Requirements
Python 3

# Contributing
Some general guidelines to keep in mind when contributing
* Rely on convention as opposed to providing extensive configuration
* Don't invent features that _might_ be needed. If you've seen an issue more than once in the past or are presented with it in the future, feel free to add functionality.
* Try to follow a [factory approach](https://en.wikipedia.org/wiki/Software_factory) where possible

# Installation
Before installation, weights files should be downloaded and placed in ./kaishi/weights/ ([link](https://drive.google.com/drive/folders/1MFYONkG83AmFqAxajT-iYM8H5Fr1W1gG?usp=sharing))

To install (it will take a few secs to copy over the weights file(s)):
```
pip install -r requirements.txt
pip install .
```

# Quick Start
To run the entire image analysis pipeline on the sample data directory, use the following commands in a python terminal:
```
from kaishi.image import Dataset
imdata = Dataset('sample_images')
imdata.run_pipeline()
imdata.report()
```

In addition, the `imdata` object contains various objects and methods to interact with the data.

At any point in the pipeline, the `imdata.files` and `imdata.filtered` objects contain results.

# A Note on Models
If you want to use the baseline convnet labeler, run the following code:
```
from kaishi.core.image.nn import Model
model = Model().model
predictions = model(stuff_you_want_to_predict)
```
This will soon be baked into the pipeline.

# A Note on Pipelines
`Dataset.pipeline.methods` and `Dataset.pipeline.args` are simply lists of functions and argument lists, respectively. You can edit this with your own custom objects simply by calling `dataset.pipeline.methods.append` and `Dataset.pipeline.args.append`, which will then be called when you run `Dataset.run_pipeline()`.
