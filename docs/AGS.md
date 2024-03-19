## Welcome to AGS data file Processing
================


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
================================

Create single group value tables geology grouped test value tables from AGS files:

``` python
#read AGS files into panda dataframws using python_AGS4
tables, headings = AGS4.AGS4_to_dataframe('path/to/file.ags')

result = ge_lib.ags.get_tables(tables, headings, 'output.ags')

```

### Create charts from AGS files

Create charts from tables geology grouped

``` python

#read AGS files into panda dataframws using python_AGS4
tables, headings = AGS4.AGS4_to_dataframe('path/to/file.ags')

result = ge_lib.ags.get_charts(tables, )

```

### Development
===============

Please refer contacts for details about the development environment and how to get involved in the project.

## Implementations
