# ge_lib
Ground Engineering common function library
[[_TOC_]]

## Introduction
`ge_lib` is a library of functions useful in ground engineering

## Setup 
  Your machine environment needs to be setup to use this libary [More..](docs/setup.md)

## Library Contents
This function library contains separates self-contained modules for a variety of engineering applications. 

### Plaxis
  Allows connection to the Plaxis Output application server and extracts results from mutiple phases [More..](docs/plaxis.md) [Examples..](examples/plaxis)

### AGS
  Summary tables and charts from AGS files using the BGS python_AGS4.py python library [More] (docs/AGS.md)

### Found
  A library of deep and shallow foundation calculations for piles and strip footing [More..](docs/found.md) [Examples..](examples/found)

### General
  Useful general purpose functions [More..](docs/general.md)

### Seismic Motions
  Functions for manipulating seismic history files [More..](docs/motions.md)

### Tunnels
  Functions for tunnel analysis and settlements [More..](docs/tunnels.md)

### Groundwater
  Functions for groundwater analysis and settlements [More..](docs/groundwater.md)

>>>
**Note**
 Each module will have separate dependencies but for simplicity a single setup requirements.txt is included. It is recommended that you create a virtual python environment to install those dependencies to. 
>>>
