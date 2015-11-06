clean:
	-rm -r build
	-rm -r dist
	-rm -r lupulo.egg-info

launch:
	cd virtual && \
	lupulo_create && \
	lupulo_start

install:
	python2 setup.py bdist_wheel
	pip2 install dist/lupulo*

uninstall:
	pip2 uninstall lupulo

all: clean uninstall install launch

.PHONY: all
