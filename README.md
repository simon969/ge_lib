# ge_lib
Ground Engineering common function library
[[_TOC_]]

## Introduction
`ge_lib` is a library of functions useful in ground engineering

### Plaxis
  Allows connection to the Plaxis Output application server and extracts results from mutiple phases

### AGS
  Using the BGS python_AGS4  

### Found
  A libraray of deep and shallow foundation calculations for piles and strip footings
  Ground resistances calculated in accordance with the <Eurocode BS EN 1997> and <BS EN 8004> 


>>>
**Note**
 This function library contains separates self contained modules for a variety of engineering applications. There are separated requirements.txt files for each module. It is recomended that you create a virtual python enviornment and only install those dependences for the module you which to use. 
>>>

## Documentation


### Juypter Notebook

We have created an example Juypter Notebook which connects to the Plaxis 2D Output program and extracts structural results dfor selected phases


[See here](./examples/Plaxis2D_StructuralResults.ipynb)

### Installation

```bash
pip install ge_lib

Installation requires Python 3.7 or later.
>>>

### Code Examples

First import the module.

```python
from python_ags4 import AGS4
```

#### Summarised multiple AGS4 files:

>>> 
**Important:** 
avsb ;qklkldk qkd
>>>

### Create tables from AGS files

Create single group value tables geology grouped test value tables from AGS files:

``` python
#read AGS files into panda dataframws using python_AGS4
tables, headings = AGS4.AGS4_to_dataframe('path/to/file.ags')

result = ge_lib.ags.get_tables(tables, headings, 'output.ags')

```

### Create charts from AGS files
``` python

#read AGS files into panda dataframws using python_AGS4
tables, headings = AGS4.AGS4_to_dataframe('path/to/file.ags')

result = ge_lib.ags.get_charts(tables, )

```

### Development

Please refer contacts for details about the development environment and how to get involved in the project.

## Implementations

This library has been used to create mutiple internal API's 
