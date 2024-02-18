# ge_lib
Ground Engineering common function library
[[_TOC_]]

## Introduction
`ge_lib` is a library of functions useful in ground engineering

## Setup 
  Your machine environment needs to be setup to use this libary [More..](doc/setup.rst)

## Library Contents
This function library contains separates self-contained modules for a variety of engineering applications. 

### Plaxis
  Allows connection to the Plaxis Output application server and extracts results from mutiple phases
  [More..](doc/plaxis.rst) [Examples..](/examples/plaxis)

### AGS
  Summary tables and charts from AGS files using the BGS python_AGS4.py python library  
  [More] (doc/ags.rst)

### Found
  A library of deep and shallow foundation calculations for piles and strip footings
  [More..](doc/found.rst) [Examples..](/examples/found)

### General
  Useful general purpose functions [More..](./doc/general.rst)

### Seismic Motions
  Functions for manipulating seismic history files [More..](/doc/motions.rst)

### Tunnels
  Functions for tunnel analysis and settlements [More..](/doc/tunnels.rst)

### Groundwater
  Functions for groundwater analysis and settlements [More..](/doc/groundwater.rst)

>>>
**Note**
 Each module will have separate dependencies but for simplicity a single setup requirements.txt is included. It is recommended that you create a virtual python environment to install those dependencies to. 
>>>
