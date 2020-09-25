## hfcMystran
Pre/Post processor for Mystran within FreeCAD.

## Background
[Mystran](https://github.com/dr-bill-c/MYSTRAN) is a general purpose finite element analysis computer program for structures that can be modeled as linear.

[FreeCAD](https://freecadweb.org) is an open source CAD/CAM solution.

## Features 
Currently this workbench contains the following tools:

###  1. Import Dat files 
Import a Dat case file and draw mesh. 

### 2. Run Mystran
Execture the `Mystran` binary which reads in the Dat file and writes the result into a Neu and a F06 file.

### 3. Show Results
Read in a Neu result file and draw the mesh and displacement.

## Prerequisites

* Mystran v11
* FreeCAD v0.19.x

## Installation
Download as hfcMystran.zip and unzip it under FreeCad's `Mod/` folder. The result is a new 'Mod/hfcMystran' folder with all the files.

This workbench is developed on Windows 10. No plan to support Linux. 

Note: Mystran excutable file must be in Windows's PATH. Under Window 10, it must be named as `Mystran.exe`. 


## Use
1. Start FreeCAD.
2. Switch to hfcMystran workbench
3. Start a New file
4. Open a Dat case file

  There is one test case under the Quickstart folder.
  
5. Solve with Mystran
6. Load result

  It will add the result into the model tree. Double click it and a Show result window will pop up. Choose the one want to view, tick View, drag the scroll bar to change the view scale.

## License
GPL v3.0 (see [LICENSE](LICENCE) file)
