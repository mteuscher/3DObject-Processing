#@ File(label='Choose X-Coordinates File', style='file') xFile
#@ File(label='Choose Y-Coordinates File', style='file') yFile
#@ File(label='Choose Z-Coordinates File', style='file') zFile

import os
from ij import IJ, ImagePlus
from ij.gui import PointRoi
from ij.plugin.frame import RoiManager

x = []
y = []
z = []

f = open(str(xFile))
for line in f:
	x.append(line.replace("\n","").split(","))
f.close()

f = open(str(yFile))
for line in f:
	y.append(line.replace("\n","").split(","))
f.close()

f = open(str(zFile))
for line in f:
	z.append(line.replace("\n","").split(","))
f.close()

x.pop(0)
y.pop(0)
z.pop(0)

imp = IJ.getImage()
rm = RoiManager()

IJ.log("Processing started")
for point in x:
	IJ.log("\\Update:Processing Object {}/{}".format(x.index(point)+1,len(x)))
	for time in point:
		if len(time) < 10 and time != 'NA':
			imp.setZ(int(round(float(z[x.index(point)][x[x.index(point)].index(time)]))))
			imp.setT(x[x.index(point)].index(time)+1)
			rm.add(imp,PointRoi(int(round(float(time))),int(round(float(y[x.index(point)][x[x.index(point)].index(time)])))),x.index(point)+1)