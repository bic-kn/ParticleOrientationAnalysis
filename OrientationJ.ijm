// @Double(label="Approximate length of particles [px]", value=50.0) lengthOfParticles
// @Double(label="Minimum coherency [%]", value=20.0) coherencyThreshold
// @OUTPUT String(label="Area Fraction of oriented particles") areaFraction

/*
 * This macro executes the OrientationJ plugin with the provided input parameters.
 * Subsequently, a mask is constructed by thresholding of the coherency image.
 * From this mask the area fraction of coherent regions is computed. Additionally,
 * a histogram of orientations within the coherent regions is kept.
 *
 * @author Stefan Helfrich (Bioimaging Center, University of Konstanz)
 * @date 02/26/2016
 */

/* TODO Compute size of tensor from calibration and provided parameter */
// cal = imp.getCalibration(); 
// x = cal.pixelWidth; // x contains the pixel width in units 
// y = cal.pixelHeight; // y contains the pixel height in units 
// z = cal.pixelDepth; // z contains the pixel (voxel) depth in units
// ij.measure.getUnits();

// Execute OrientationJ
run("OrientationJ Distribution", "log=0.0 tensor="+ lengthOfParticles/2 +
	" gradient=1 min-coherency="+ coherencyThreshold +" min-energy=0.0 s-mask=on " +
	"s-orientation=on s-distribution=on hue=Orientation sat=Coherency bri=Original-Image");

/* Close unused windows */
// Keep "S-Distribution"
lastImageId = getImageID();
distributionId = lastImageId;

// Close "S-Orientation"
selectImage(++lastImageId);
close();

// Keep "S-Mask"
selectImage(++lastImageId);
maskId = getImageID();

// Close "Orientation"
selectImage(++lastImageId);
close();

// Get selection and compute area
selectImage(maskId);
setThreshold(0.5, 1.0);
run("Set Measurements...", "area area_fraction limit redirect=None decimal=3");
run("Measure");

/* Close "Results" */
// TODO Check if a "Results" window is open
close("Results");

// Print Area%
areaFraction = toString(getResult("%Area"))+"%";

// TODO Reset measurements

// Close "S-Mask"
close();
