# File datasets
If there's a particular data type you are working with, it's usually better to use the type-specific dataset object. However, there are still a few core operations that can be performed on generic files.

## Initializing datasets
Let's start by creating a simple dataset of text files.


```python
import os
outdir = "toy_files"
os.mkdir(outdir)

file1 = "file1_contents"
file2 = "file2_contents"
file2_duplicate = "file2_contents"
file3 = "file3_contents"
with open(outdir + "/1.file", "w") as fd:
    fd.write(file1)
with open(outdir + "/2.file", "w") as fd:
    fd.write(file2)
with open(outdir + "/2_dup.file", "w") as fd:
    fd.write(file2_duplicate)
with open(outdir + "/3.file", "w") as fd:
    fd.write(file3)
```


```python
from kaishi.core.dataset import FileDataset
fd = FileDataset(outdir)
fd.file_report()
```

    Current file list:
    +-------+------------+------------------------+--------+
    | Index | File Name  | Children               | Labels |
    +-------+------------+------------------------+--------+
    |   0   |   3.file   |     {'duplicates': []} |   []   |
    |   1   |   2.file   |     {'duplicates': []} |   []   |
    |   2   | 2_dup.file |     {'duplicates': []} |   []   |
    |   3   |   1.file   |     {'duplicates': []} |   []   |
    +-------+------------+------------------------+--------+
    Filtered files:
    +-----------+---------------+
    | File Name | Filter Reason |
    +-----------+---------------+
    +-----------+---------------+


## File procesing pipelines
There are fewer components available for files compared to other types, as the other types inherit from the FileGroup class. However, there are still plenty of options available to perform some common operations.


```python
fd.get_pipeline_options()
```




    ['FilterByLabel',
     'FilterByRegex',
     'FilterDuplicateFiles',
     'FilterSubsample',
     'LabelerValidationAndTest']




```python
fd.configure_pipeline(["FilterDuplicateFiles", "FilterSubsample"])
print(fd.pipeline)
```

    Kaishi pipeline: 
    0: FilterDuplicateFiles
    1: FilterSubsample
         N: None
         seed: None
    



```python
fd.pipeline.components[1].configure(N=2, seed=42)
print(fd.pipeline)
```

    Kaishi pipeline: 
    0: FilterDuplicateFiles
    1: FilterSubsample
         N: 2
         seed: 42
    



```python
fd.run_pipeline()
fd.file_report()
```

    Current file list:
    +-------+-----------+----------------------------------+--------+
    | Index | File Name | Children                         | Labels |
    +-------+-----------+----------------------------------+--------+
    |   0   |   3.file  |     {'duplicates': []}           |   []   |
    |   1   |   2.file  |     {'duplicates': [2_dup.file]} |   []   |
    +-------+-----------+----------------------------------+--------+
    Filtered files:
    +------------+---------------+
    | File Name  | Filter Reason |
    +------------+---------------+
    | 2_dup.file |   duplicates  |
    |   1.file   |   subsample   |
    +------------+---------------+

