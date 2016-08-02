Particle Orientation Analysis Script
====================================

The Particle Orientation Analysis script computes an estimate of the degree of orientation in a particle mixture. This quantity is computed as the area fraction that is covered by oriented domains in EM images using [OrientationJ](http://bigwww.epfl.ch/demo/orientation/).

# How to install the script
1. Install [OrientationJ](http://bigwww.epfl.ch/demo/orientation/) according to the provided instructions
2. Drop *Particle\_Orientation\_Analysis.py* into the *plugins/* folder of your Fiji installation

# How to use the script
1. Open image you want to analyze
2. Convert it to 8-bit grey scale (*Image > Type > 8-bit*)
3. Set ROIs that you want to discard in the computations
    - Make selection
    - Add selection to overlay (*Image > Overlay > Add Selection...* or `Ctrl+B`)
    - When images are saved as TIFF, the overlay (as well as the scaling information) is stored
3. Run *Plugins > Particle Orientation Analysis*
4. Evaluate output
    * Area fraction of oriented particles in %
    * Histogram of orientations in the areas with a high coherency (**currently, this does not discard holes, i.e. regions of the image with a high energy value**)

# How to set the scale of an image
1. Open EM image
2. Make a line selection on the provided scale bar (hold down shift for horizontal line)
3. Open *Analyse > Set Scale*
4. Provide *Known distance* from scale bar
5. Set *Unit of length*

or

1. Open EM image
2. Open *Analyse > Set Scale*
3. Set *Distance in pixels* to 1
3. Provide *Known distance* from "Pixel Size" property in the EM image (in units)
4. Set *Unit of length*

# Miscellaneous
* **map0to180.lut** maps values near 180 and 0 degrees to the same grey value. Apply to an open image via *Image > Color > Edit LUT... > Open...*
* **TestWindowSizes.ijm** executes OrientationJ with various window sizes (minor changes compared to the one [provided](http://bigwww.epfl.ch/demo/orientation/tree-orientation.txt) by the developers)
