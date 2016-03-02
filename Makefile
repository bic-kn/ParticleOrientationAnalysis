all: README.pdf zip

README.pdf:
	pandoc README.md --latex-engine=xelatex --variable fontsize=10pt --variable documentclass=article -o README.pdf

zip:
	zip Particle_Orientation_Analysis.zip Particle_Orientation_Analysis.py map0to180.lut README.pdf

clean:
	rm README.pdf
	rm Particle_Orientation_Analysis.zip
