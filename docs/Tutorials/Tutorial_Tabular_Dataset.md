# Tabular Datasets
Tabular datasets in this context are directories of files (any variant of .csv or .json is accepted).

## Initializing datasets
Let's start by creating our own toy dataset (with one duplicate, i.e. files 1 and 2)


```python
import pandas as pd
import os
outdir = "toy_csv"
os.mkdir(outdir)

csv1 = """
"Index", "Living Space (sq ft)", "Beds", "Baths"
 1, 2222, 3, 3.5
 2, 1628, 3, 2
 3, 3824, 5, 4
 4, 1137, 3, 2
 5, 3560, 6, 4
 6, 2893, 4, 3
 7, 3631, 4, 3
 8, 2483, 4, 3
 9, 2400, 4, 4
10, 1997, 3, 3
"""
csv2 = """
"Index", "Living Space (sq ft)", "Beds", "Baths"
 1, 2222, 3, 3.5
 2, 1628, 3, 2
 3, 3824, 5, 4
 4, 1137, 3, 2
 5, 3560, 6, 4
 6, 2893, 4, 3
 7, 3631, 4, 3
 8, 2483, 4, 3
 9, 2400, 4, 4
10, 1997, 3, 3
"""
csv3 = """
"Index", "Living Space (sq ft)", "Beds", "Baths"
11, 2222, 3, 3.5
12, 1628, 3, 2
13, 3824, 5, 4
14, 1137, 3, 2
15, 3560, 6, 4
16, 2893, 4, 3
17, 3631, 4, 3
18, 2483, 4, 3
19, 2400, 4, 4
20, 1997, 3, 3
"""
with open(outdir + "/1.csv", "w") as fd:
    fd.write(csv1)
with open(outdir + "/2.csv", "w") as fd:
    fd.write(csv2)
with open(outdir + "/3.csv", "w") as fd:
    fd.write(csv3)
```


```python
from kaishi.tabular.dataset import TabularDataset
td = TabularDataset(outdir)
td.file_report()
```

    Current file list:
    +-------+-----------+------------------------+--------+
    | Index | File Name | Children               | Labels |
    +-------+-----------+------------------------+--------+
    |   0   |   1.csv   |     {'duplicates': []} |   []   |
    |   1   |   3.csv   |     {'duplicates': []} |   []   |
    |   2   |   2.csv   |     {'duplicates': []} |   []   |
    +-------+-----------+------------------------+--------+
    Filtered files:
    +-----------+---------------+
    | File Name | Filter Reason |
    +-----------+---------------+
    +-----------+---------------+


## Interaction with datasets
There are several ways to interact with tabular datasets. Let's start by looking at a detailed report.


```python
td.report()
```

    
    Dataframe 0
    source: /Users/mwharton/Code/kaishi/notebooks/toy_csv/1.csv
    ====================================
    NO DATA OR NOT LOADED (try running 'dataset.load_all()')
    
    
    Dataframe 1
    source: /Users/mwharton/Code/kaishi/notebooks/toy_csv/3.csv
    ====================================
    NO DATA OR NOT LOADED (try running 'dataset.load_all()')
    
    
    Dataframe 2
    source: /Users/mwharton/Code/kaishi/notebooks/toy_csv/2.csv
    ====================================
    NO DATA OR NOT LOADED (try running 'dataset.load_all()')
    


Our data weren't loaded, let's fix that and try again


```python
td.load_all()
td.report()
```

    
    Dataframe 0
    source: /Users/mwharton/Code/kaishi/notebooks/toy_csv/1.csv
    ====================================
    4 columns: ['Index', ' "Living Space (sq ft)"', ' "Beds"', ' "Baths"']
    
    ---  Column 'Index'
    count    10.00000
    mean      5.50000
    std       3.02765
    min       1.00000
    25%       3.25000
    50%       5.50000
    75%       7.75000
    max      10.00000
    Name: Index, dtype: float64
    
    ---  Column ' "Living Space (sq ft)"'
    count      10.00000
    mean     2577.50000
    std       894.97725
    min      1137.00000
    25%      2053.25000
    50%      2441.50000
    75%      3393.25000
    max      3824.00000
    Name:  "Living Space (sq ft)", dtype: float64
    
    ---  Column ' "Beds"'
    count    10.000000
    mean      3.900000
    std       0.994429
    min       3.000000
    25%       3.000000
    50%       4.000000
    75%       4.000000
    max       6.000000
    Name:  "Beds", dtype: float64
    
    ---  Column ' "Baths"'
    count    10.000000
    mean      3.150000
    std       0.747217
    min       2.000000
    25%       3.000000
    50%       3.000000
    75%       3.875000
    max       4.000000
    Name:  "Baths", dtype: float64
    
    ***** Fraction of missing data in each column *****
    Index: 0.0
     "Living Space (sq ft)": 0.0
     "Beds": 0.0
     "Baths": 0.0
    
    
    Dataframe 1
    source: /Users/mwharton/Code/kaishi/notebooks/toy_csv/3.csv
    ====================================
    4 columns: ['Index', ' "Living Space (sq ft)"', ' "Beds"', ' "Baths"']
    
    ---  Column 'Index'
    count    10.00000
    mean     15.50000
    std       3.02765
    min      11.00000
    25%      13.25000
    50%      15.50000
    75%      17.75000
    max      20.00000
    Name: Index, dtype: float64
    
    ---  Column ' "Living Space (sq ft)"'
    count      10.00000
    mean     2577.50000
    std       894.97725
    min      1137.00000
    25%      2053.25000
    50%      2441.50000
    75%      3393.25000
    max      3824.00000
    Name:  "Living Space (sq ft)", dtype: float64
    
    ---  Column ' "Beds"'
    count    10.000000
    mean      3.900000
    std       0.994429
    min       3.000000
    25%       3.000000
    50%       4.000000
    75%       4.000000
    max       6.000000
    Name:  "Beds", dtype: float64
    
    ---  Column ' "Baths"'
    count    10.000000
    mean      3.150000
    std       0.747217
    min       2.000000
    25%       3.000000
    50%       3.000000
    75%       3.875000
    max       4.000000
    Name:  "Baths", dtype: float64
    
    ***** Fraction of missing data in each column *****
    Index: 0.0
     "Living Space (sq ft)": 0.0
     "Beds": 0.0
     "Baths": 0.0
    
    
    Dataframe 2
    source: /Users/mwharton/Code/kaishi/notebooks/toy_csv/2.csv
    ====================================
    4 columns: ['Index', ' "Living Space (sq ft)"', ' "Beds"', ' "Baths"']
    
    ---  Column 'Index'
    count    10.00000
    mean      5.50000
    std       3.02765
    min       1.00000
    25%       3.25000
    50%       5.50000
    75%       7.75000
    max      10.00000
    Name: Index, dtype: float64
    
    ---  Column ' "Living Space (sq ft)"'
    count      10.00000
    mean     2577.50000
    std       894.97725
    min      1137.00000
    25%      2053.25000
    50%      2441.50000
    75%      3393.25000
    max      3824.00000
    Name:  "Living Space (sq ft)", dtype: float64
    
    ---  Column ' "Beds"'
    count    10.000000
    mean      3.900000
    std       0.994429
    min       3.000000
    25%       3.000000
    50%       4.000000
    75%       4.000000
    max       6.000000
    Name:  "Beds", dtype: float64
    
    ---  Column ' "Baths"'
    count    10.000000
    mean      3.150000
    std       0.747217
    min       2.000000
    25%       3.000000
    50%       3.000000
    75%       3.875000
    max       4.000000
    Name:  "Baths", dtype: float64
    
    ***** Fraction of missing data in each column *****
    Index: 0.0
     "Living Space (sq ft)": 0.0
     "Beds": 0.0
     "Baths": 0.0
    


To look at a specific file object, you can access via either index or key


```python
td.files[0].df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Index</th>
      <th>"Living Space (sq ft)"</th>
      <th>"Beds"</th>
      <th>"Baths"</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>2222</td>
      <td>3</td>
      <td>3.5</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1628</td>
      <td>3</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3824</td>
      <td>5</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1137</td>
      <td>3</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>3560</td>
      <td>6</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>2893</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>3631</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>2483</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>2400</td>
      <td>4</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>1997</td>
      <td>3</td>
      <td>3.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
td["1.csv"].df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Index</th>
      <th>"Living Space (sq ft)"</th>
      <th>"Beds"</th>
      <th>"Baths"</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>2222</td>
      <td>3</td>
      <td>3.5</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1628</td>
      <td>3</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3824</td>
      <td>5</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1137</td>
      <td>3</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>3560</td>
      <td>6</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>2893</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>3631</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>2483</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>2400</td>
      <td>4</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>1997</td>
      <td>3</td>
      <td>3.0</td>
    </tr>
  </tbody>
</table>
</div>



## Tabular data processing pipelines

Let's see the pipeline options


```python
td.get_pipeline_options()
```




    ['FilterByLabel',
     'FilterByRegex',
     'FilterDuplicateFiles',
     'FilterDuplicateRowsAfterConcatenation',
     'FilterDuplicateRowsEachDataframe',
     'FilterInvalidFileExtensions',
     'FilterSubsample',
     'LabelerValidationAndTest',
     'AggregatorConcatenateDataframes']



Now let's configure our own pipeline and run it


```python
td.configure_pipeline(["FilterDuplicateFiles", "AggregatorConcatenateDataframes"])
print(td.pipeline)
td.run_pipeline()
```

    Kaishi pipeline: 
    0: FilterDuplicateFiles
    1: AggregatorConcatenateDataframes
    


As expected, the duplicate file was filtered


```python
td.file_report()
```

    Current file list:
    +-------+-----------+-----------------------------+--------+
    | Index | File Name | Children                    | Labels |
    +-------+-----------+-----------------------------+--------+
    |   0   |   1.csv   |     {'duplicates': [2.csv]} |   []   |
    |   1   |   3.csv   |     {'duplicates': []}      |   []   |
    +-------+-----------+-----------------------------+--------+
    Filtered files:
    +-----------+---------------+
    | File Name | Filter Reason |
    +-----------+---------------+
    |   2.csv   |   duplicates  |
    +-----------+---------------+


But what about the concatenated dataframe? When Kaishi pipeline components create artifacts, they are added to the artifacts member of a dataset.


```python
print(td.artifacts.keys())
```

    dict_keys(['df_concatenated'])



```python
td.artifacts["df_concatenated"]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Index</th>
      <th>"Living Space (sq ft)"</th>
      <th>"Beds"</th>
      <th>"Baths"</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>2222</td>
      <td>3</td>
      <td>3.5</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1628</td>
      <td>3</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3824</td>
      <td>5</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1137</td>
      <td>3</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>3560</td>
      <td>6</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>2893</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>3631</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>2483</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>2400</td>
      <td>4</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>1997</td>
      <td>3</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>11</td>
      <td>2222</td>
      <td>3</td>
      <td>3.5</td>
    </tr>
    <tr>
      <th>11</th>
      <td>12</td>
      <td>1628</td>
      <td>3</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>13</td>
      <td>3824</td>
      <td>5</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>14</td>
      <td>1137</td>
      <td>3</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>15</td>
      <td>3560</td>
      <td>6</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>16</td>
      <td>2893</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>17</td>
      <td>3631</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>18</td>
      <td>2483</td>
      <td>4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>19</td>
      <td>2400</td>
      <td>4</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>20</td>
      <td>1997</td>
      <td>3</td>
      <td>3.0</td>
    </tr>
  </tbody>
</table>
</div>



This ultimately sets the framework for being able to manipulate your own tabular data sets and add custom functionality, without the hassle of dealing with the boring and monotonous ETL steps.
