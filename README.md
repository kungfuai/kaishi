# Kaishi
# 開始
Tool kit to accelerate the initial phases of exploratory data analysis, as well as to enable rapid dataset preparation for downstream tasks.

![](https://github.com/kungfuai/kaishi/workflows/build/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/kaishi/badge/?version=latest)](https://kaishi.readthedocs.io/en/latest/?badge=latest)
<!--[![PyPI Latest Release](https://img.shields.io/pypi/v/pandas.svg)](https://pypi.org/project/kaishi/)-->

## Brief Overview
The advent of deep learning provides opportunities to detect issues present in data that would otherwise be extremely difficult to detect algorithmically (unnatural image aspect ratios, subjectively similar data, etc.). Kaishi attempts to take advantage of this to help you get to know your data subjectively and intimately on the front end, thus saving time that would have been spent debugging later on. There are, of course, many standard tools built in as well (deduplication, artifact detection, merge operations, etc.) that can all be chained to provide powerful automated data engineering.

Two data types (images and tabular data) are currently implemented, but more (e.g. signals, video, etc.) will be added in future releases. A lot of functionality for new data types exists out of the box though, especially when it comes to file handling.

# Requirements
Python 3.6+

# Installation
To install (it will take a few secs to copy over the weights file(s)):
```
pip install -r requirements.txt
pip install .
```

# Quick Start
The only requirement to use Kaishi is that your dataset is a directory of files (support for other dataset types to come). It is first and foremost a discovery tool, and thus is not optimized for huge data sets. Try working with a subset to start exploring.

To run a simple image processing pipeline, try the below:
```
from kaishi.image.dataset import ImageDataset
imdata = ImageDataset('tests/data/image', recursive=True)
imdata.configure_pipeline(["FilterInvalidFileExtensions", "FilterDuplicateFiles", "FilterSimilar"])
# You can also use imdata.configure_pipeline() without arguments to get guided input
imdata.run_pipeline()
imdata.file_report()
```

You will get command line output that looks like the below:
```
Current file list:
+-------+----------------------+-------------------------------------------------+--------+
| Index |      File Name       |                     Children                    | Labels |
+-------+----------------------+-------------------------------------------------+--------+
|   0   |    real_near2.jpg    | {'duplicates': [], 'similar': [real_near1.jpg]} |   []   |
|   1   | sample_duplicate.jpg |   {'duplicates': [sample.jpg], 'similar': []}   |   []   |
+-------+----------------------+-------------------------------------------------+--------+
Filtered files:
+---------------------------------+-----------------------+
|            File Name            |     Filter Reason     |
+---------------------------------+-----------------------+
| empty_unsupported_extension.gif | unsupported_extension |
|            sample.jpg           |       duplicates      |
|          real_near1.jpg         |        similar        |
+---------------------------------+-----------------------+
```

Finally, you can save your modified datset in a new directory with the below command:
```
imd.save('output_directory')
```

This process is agnostic to the data type you have chosen. For instance:
```
from kaishi.tabular.dataset import TabularDataset
td = TabularDataset('tests/data/tabular', recursive=True)
td.configure_pipeline(['FilterDuplicateFiles'])
td.run_pipeline()
td.save('output_directory_tabular')
```

Some pipeline components are, of course, unique to a particular data type. To see which are available:
```
imd.get_pipeline_options()
# or td.get_pipeline_options()
```

Finally, if you want operations that apply to files in general, you can use the below:
```
from kaishi.core.dataset import FileDataset
fd = FileDataset('your_directory')
...
```

# Documentation
For more info, see our [documentation on ReadTheDocs](https://kaishi.readthedocs.io/en/latest/)
