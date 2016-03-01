/*
 * OrientationJ
 *
 * This macro is an example how to call the OrientationJ plugin.
 * It produces a series of slowly variation of the structure tensor window
 *
 * Daniel Sage
 * Biomedical Imaging Group (BIG), Ecole Polytechnique Federale de Lausanne (EPFL), Swizterland
 * 
 * 24 January 2009
 *
 * Full information http://bigwww.epfl.ch/demo/orientation/
 *
 * You'll be free to use this software for research purposes, but you should not redistribute it 
 * without our consent. In addition, we expect you to include a citation or acknowledgement 
 * whenever you present or publish results that are based on it.
 *
 */

rename("in");
n = 20;
for ( i=3; i<n; i++) { 
	selectWindow("in");
	a = i;
	run("OrientationJ Analysis", "log=0.0 tensor=" + a + " gradient=1 color-survey=on hue=Orientation sat=Coherency bri=Original-Image ");
}
run("Images to Stack", "title=Color-survey");
selectWindow("in");
close();