# @OpService ops
# @DisplayService displays
# @ImagePlus imp
# @Double(label="Approximate length of particles [units]", value=50.0) lengthOfParticles
# @Double(label="Minimum coherency [%]", value=20.0) coherencyThreshold
# @OUTPUT String(label="Area Fraction of oriented particles") areaFraction

# This macro executes the OrientationJ plugin with the provided input parameters.
# Subsequently, a mask is constructed by thresholding of the coherency image.
# From this mask the area fraction of coherent regions is computed. Additionally,
# a histogram of orientations within the coherent regions is kept.
#
# @author Stefan Helfrich (Bioimaging Center, University of Konstanz)
# @date 03/01/2016

import math;
from ij import IJ, WindowManager;
from ij.plugin.filter import Analyzer;
from ij.measure import Measurements, ResultsTable;
from net.imglib2.img.display.imagej import ImageJFunctions;
from net.imglib2.type.logic import BitType;
from net.imglib2.type.numeric.real import DoubleType, FloatType;
from net.imglib2.meta import ImgPlus;
from net.imagej.ops import Ops;

### Compute size of tensor from calibration and provided parameter ###
cal = imp.getCalibration(); 
x = cal.pixelWidth; # x contains the pixel width in units 
if IJ.debugMode:
  print("Calibration pixel width: "+str(x));

# Assume that scaling in x and y direction is the same
tensorSpan = math.floor((lengthOfParticles/x)/2);
if IJ.debugMode:
  print("Tensor span: "+str(tensorSpan)+"px");

### Execute OrientationJ ###
IJ.run(imp, "OrientationJ Distribution", "log=0.0 tensor="+ str(tensorSpan) + " gradient=1 " +
	"min-coherency="+ str(coherencyThreshold) +" min-energy=0.0 energy=on harris-index=on s-mask=on " +
	"s-orientation=on s-distribution=on hue=Orientation sat=Coherency bri=Original-Image ");

IJ.run(imp, "OrientationJ Analysis", "log=0.0 tensor="+ str(tensorSpan) + " gradient=1 energy=on hue=Orientation sat=Coherency bri=Original-Image ");

### Close unused windows ###
for imp in map(WindowManager.getImage, WindowManager.getIDList()):
  title = imp.getTitle();
  if title.startswith("Orientation"):
  	# Close "Orientation"
	imp.close();
  
  if title.startswith("S-Mask"):
  	# Keep "S-Mask"
	maskImp = imp;
  
  if title.startswith("S-Orientation"):
  	# Close "S-Orientation"
	imp.close();
  
  if title.startswith("Energy"):
  	# Keep "Energy"
	energyImp = imp;

### Remove holes from image ###
# Threshold energyImp
wrappedImg = ImageJFunctions.wrap(energyImp);
output = ops.create().img(wrappedImg, BitType());
ops.threshold().apply(output, wrappedImg, FloatType(0.20));

# Invert, b/c we want to have lower energy regions
invertedOutput = ops.create().img(wrappedImg, BitType());
ops.image().invert(invertedOutput, output);

if IJ.debugMode:
  displays.createDisplay("energy-thresholded", ImgPlus(invertedOutput));

# Convert mask to binary image
wrappedMask = ImageJFunctions.wrap(maskImp);
bitMask = ops.create().img(wrappedImg, BitType());
ops.convert().bit(bitMask, wrappedMask);

if IJ.debugMode:
  displays.createDisplay("coherency-thresholded", ImgPlus(bitMask));

# AND with maskImp
newMask = ops.create().img(wrappedImg, BitType());
newMaskCursor = newMask.cursor();
outputCursor = invertedOutput.cursor();
maskCursor = bitMask.cursor();

while (newMaskCursor.hasNext()):
  outputPixel = outputCursor.next().get();
  maskPixel = maskCursor.next().get();
  newMaskCursor.next().set(BitType(outputPixel and maskPixel));

# TODO map with and op
#andOp = ops.op(Ops.Logic.And, BitType(), BitType());
#ops.map(newMask, ImageJFunctions.wrap(maskImp), output, andOp);
#displays.createDisplay("combined_output", ImgPlus(newMask));

# Compute area from coherency mask
newMaskImp = ImageJFunctions.wrapUnsignedByte(newMask, "New mask");
newMaskImp.getProcessor().setThreshold(1.0, 1.5, False); # [0.5, 1.0] does not work due to rounding problems
rt = ResultsTable();
analyzer = Analyzer(newMaskImp, Measurements.AREA | Measurements.LIMIT, rt);
analyzer.measure();

# Compute area from energy mask 
energyMaskImp = ImageJFunctions.wrapUnsignedByte(invertedOutput, "Energy mask");
energyMaskImp.getProcessor().setThreshold(1.0, 1.5, False); # [0.5, 1.0] does not work due to rounding problems
rtEnergy = ResultsTable();
analyzerEnergy = Analyzer(energyMaskImp, Measurements.AREA | Measurements.LIMIT, rtEnergy);
analyzerEnergy.measure();

# Print Area% (through SciJava OUTPUT, see L5)
if IJ.debugMode:
  print("Coherency area: "+str(rt.getValueAsDouble(rt.getColumnIndex("Area"), rt.size()-1)));
  print("Energy area: "+str(rtEnergy.getValueAsDouble(rtEnergy.getColumnIndex("Area"), rtEnergy.size()-1)));

areaCoherency = rt.getValueAsDouble(rt.getColumnIndex("Area"), rt.size()-1);
areaEnergy = rtEnergy.getValueAsDouble(rtEnergy.getColumnIndex("Area"), rtEnergy.size()-1);
areaFraction = str(areaCoherency/areaEnergy*100.0)+"%";

# Close "S-Mask"
maskImp.close();
# Close "Energy"
energyImp.close();
