# @net.imagej.Dataset input
# @OUTPUT ImgPlus output
# @OpService ops

# Apply FFT
output = ops.filter().fft().FFTImg(input.getImgPlus());

# Apply polar transformation
#run("Polar Transformer", "method=Polar degrees=360 default_center for_polar_transforms,");
#
#for (i=0; i<x; ++i) {
#	makeLine(i, 0, i, 360);
#	run("Measure");
#}