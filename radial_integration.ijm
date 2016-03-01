// FFT of image
run("FFT");

// Apply polar transformation
run("Polar Transformer", "method=Polar degrees=360 default_center for_polar_transforms,");

for (i=0; i<getWidth(); ++i) {
	makeLine(i, 0, i, 360);
	run("Measure");
}