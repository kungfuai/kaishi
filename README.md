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
To install:
```
pip install -r requirements.txt
python setup.py install
```

# Quick Start
To run the entire image analysis pipeline on the sample data directory, use the following commands in a python terminal:
```
from kaishi.image import Dataset
imdata = Dataset('sample_images')
imdata.run_pipeline()
imdata.report()
```
If successful, a report like the below will be displayed:
```
Valid files:
	real_same1.jpg
Invalid files:
	unsupported_extension:
		file.gif
		file1
		fil2
		file3
	invalid_header:
		file.bmp
		file.jpg
		file.jpeg
	duplicates:
		real_same2.jpg
```
In addition, the `imdata` object contains various objects and methods to interact with the data.

At any point in the pipeline, the `imdata.files` and `imdata.filtered` objects contain results.

# A Note on Pipelines
`Dataset.pipeline.methods` and `Dataset.pipeline.args` are simply lists of functions and argument lists, respectively. You can edit this with your own custom objects simply by calling `dataset.pipeline.methods.append` and `Dataset.pipeline.args.append`, which will then be called when you run `Dataset.run_pipeline()`.
