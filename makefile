#test: face.mdl  main.py matrix.py mdl.py display.py draw.py gmath.py
all:
	python3 main.py face.mdl
	display pic.ppm
clean:
	rm *pyc *out parsetab.py

clear:
	rm *pyc *out parsetab.py *ppm
	