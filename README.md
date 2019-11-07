# kaishi
Tool kit to accelerate the initial phases of exploratory data analysis.

"kaishi" is the Chinese word for "begin", often used to mark the start a Kung Fu fight.

# Requirements
Python 3

# Installation
To install:
```
pip install -r requirements.txt
pip install ./kaishi
```

# Quick Start
To run the entire image analysis pipeline on the sample data directory, use the following commands in a python terminal:
```
from kaishi.image import analyze_dir
imdata = analyze_dir('sample_images')
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

# Fine control
All parts of the above pipeline can be interacted with directly and independently. The `files` and `filtered` members of a dataset object keep lists of files based on applied filters.

```
from kaishi.image import dataset
imdata = dataset()
```
From here you can use the `load_dir(dirname)` and `show_available_filters()` methods to get started. After running filters, you can intermittently run `imdata.report()` to see intermediate results.

When complete, the `imdata.files` and `imdata.filtered` objects contain results.
