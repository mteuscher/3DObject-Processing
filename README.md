# 3DObject-Processing
Scripts for subsequent analysis of Objects from 3D Objects counter plugin (Fiji)

## extract similar objects.py
Run in normal Python environment. Uses a reference timepoint to extract coordinates of the Objects detected by 3D Object counter. Then look in all files of the folder for the same coordinates within a certain tolerance and write results to a new file. This is for now determined by the column the values are in. So depending what results you choose to obtain it might be different than used by this script.

## Add to Roi-Manager.py
Run from within Fiji. Add the found values from the ouput file of 'extract similar objects.py' to the ROI Manager of Fiji
