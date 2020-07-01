# 3DObject-Processing
Scripts for subsequent analysis of Objects from 3D Objects counter plugin (Fiji)

## 3D_Objects_Counter-MT-2.0.2-SNAPSHOT-MT.jar
Modified 3D Objects Counter Plugin to include ID, Min Dist. to Surf., Max Dist. to Surf. and the ratio of Max/Min Dist. to surf in the results table. Copy in Plugins folder of Fiji. Fork at https://github.com/mteuscher/3D_Objects_Counter

## 3DOC - MT-version.ijm
ImageJ Macro to include all required steps for extracting the nuclei from source images. Specific for fused/deconvolved images from Cologne SPIM. Some parameters need to be adjusted each time (see comments in script)
Need the modified 3D Objects Counter Plugin

## 3DOC -regular version.ijm
Does the same as 3DOC - MT-version.ijm, but uses the official 3D Object Counter Plugin (https://github.com/fiji/3D_Objects_Counter)

## extract similar objects - no filtering.py
Run in normal Python environment. Uses a reference timepoint to extract coordinates of the Objects detected by 3D Object counter. Then look in all files of the folder for the same coordinates within a certain tolerance and write results to a new file. This is for now determined by the column the values are in. So depending what results you choose to obtain and which 3DOC counter version you use adaptations might be needed.

## extract similar objects - duplicate and spike removal.py
The same as extract similar object, but includes filters for:
### Duplicates
Remove all hits for a file/timepoint if more than 1 is found
### Spikes
Iterate over each object and remove all points that exceed a certain threshold
### Coverage
Remove objects, that are not represented in a defined percentage of files/timepoints analyzed.

## Add to Roi-Manager.py
Run from within Fiji. Add the found values from the ouput file of 'extract similar objects.py' to the ROI Manager of Fiji
