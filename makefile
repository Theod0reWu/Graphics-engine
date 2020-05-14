#test: face.mdl  main.py matrix.py mdl.py display.py draw.py gmath.py
all:
	python3 main.py face.mdl
	convert animation/simple_100* -delay 1.7 animation/simple.gif
	display animation/simple.gif
	
clean:
	rm *pyc *out parsetab.py

clear:
	rm *pyc *out parsetab.py *ppm
	