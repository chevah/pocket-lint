PYTHON = python

build:
	$(PYTHON) setup.py build

check: build
	$(PYTHON) test.py -v

changelog:
	@if test -d .bzr/branch; then \
	    echo "<Generated by bzr log --log-format=gnu>" > ChangeLog; \
	    echo "" >> ChangeLog; \
		BZR_PLUGIN_PATH=bzr_plugins bzr log --log-format=gnu >> ChangeLog; \
	fi

manifest: changelog
	$(PYTHON) setup.py sdist --manifest-only

dist: build manifest
	$(PYTHON) setup.py sdist

clean:
	$(PYTHON) setup.py clean
	rm -r build/

distclean: clean
	rm -r dist/ MANIFEST ChangeLog

.PHONY: build check changelog manifest dist clean distclean
