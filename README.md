# How to install the macro
1. Install OrientationJ from BIG homepage (according to their instructions)
2. Drop *Particle\_Orientation\_Analysis.ijm* into the *plugins/* folder of your Fiji installation

# How to use the macro
1. Open image you want to analyze
2. Run *Plugins > Particle Orientation Analysis*
3. Evaluate output
    * Area fraction of oriented particles in %
    * Histogram of orientations in the areas with a high coherency (**currently, this does not discard holes, i.e. regions of the image with a high energy**)

# Miscellaneous
* **radial_integration.py** is not properly working at the moment
* **radial_integration.ijm** performs an FFT on the input image, converts the FFT to polar coordinates (requires plugin [Polar Transformer](http://rsb.info.nih.gov/ij/plugins/polar-transformer.html)), and radially integrates along the distance to center axis
* **map0to180.lut** maps values near 180 and 0 degrees to the same grey value. Apply to an open image via *Image > Color > Edit LUT... > Open...*
* **TestWindowSizes.ijm** executes OrientationJ with various window sizes (minor changes compared to the one [provided](http://bigwww.epfl.ch/demo/orientation/tree-orientation.txt) by the developers)
