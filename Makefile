PYTHON = python
VERSION = $(shell $(PYTHON) setup.py -V)

build:
	$(PYTHON) setup.py build

test:
	#$(PYTHON) test.py
	$(PYTHON) -m unittest discover pocketlint

check: build test

changelog:
	@if test -d .bzr/branch; then \
	    echo "<Generated by bzr log --log-format=gnu>" > ChangeLog; \
	    echo "" >> ChangeLog; \
		BZR_PLUGIN_PATH=bzr_plugins bzr log --log-format=gnu >> ChangeLog; \
	fi

manifest: changelog
	$(PYTHON) setup.py sdist --manifest-only

dist: build manifest
	$(PYTHON) setup.py signed_sdist

install:
	$(PYTHON) setup.py install

clean:
	$(PYTHON) setup.py clean
	rm -r build/

distclean: clean
	rm -r dist/ MANIFEST ChangeLog

.PHONY: build check changelog manifest dist clean distclean
