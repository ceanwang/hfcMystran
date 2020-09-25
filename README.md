## hfcMystran
Pre/Post processor for Mystran within FreeCAD

## Background
[Mystran](https://github.com/dr-bill-c/MYSTRAN) Mystran is a general purpose finite element analysis computer program for structures that can be modeled as linear.

[FreeCAD](https://freecadweb.org) is an open source CAD/CAM solution.

## Features 
Currently this workbench contains the following tools:

###  Reading Dat files 
The ability to read in an Dat case file and draw mesh. 

### Run Mystran
Execture the `Mystran` binary which reads in the Dat file and writes the result into a Neu and a F06 file.

### Show Results
Read in a Neu result file and draw the mesh and displacement.

## Prerequisites

* Mystran
* FreeCAD v0.19.x

## Installation
This workbench is developed on Windows 10.  

Note: Mystran excutable file must be in Windows's PATH. Under Window 10, it must be named as `Mystran.exe`. 

Download as hfcMystran.zip and unzip it under FreeCad's `Mod/` folder. The result is a new 'Mod/hfcMystran' folder with all the codes.

## License
GPL v3.0 (see [LICENSE](LICENCE) file)
