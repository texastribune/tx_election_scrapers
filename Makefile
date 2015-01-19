APP=tx_elections_scrapers
VERSION=0.3.0


help:
	@echo "make commands:"
	@echo "  make help    - this help"
	@echo "  make clean   - remove temporary files in .gitignore"
	@echo "  make test    - run test suite"
	@echo "  make install - install this package"
	@echo "  make release - drop and recreate the database"

clean:
	find . -name "*.pyc" -delete
	find . -name ".DS_Store" -delete
	rm -rf *.egg
	rm -rf *.egg-info
	rm -rf __pycache__
	rm -rf build
	rm -rf dist
	rm -rf MANIFEST

# kind of does a lot, but I want to make sure the CLI tools work too
test: install
	python -m unittest discover
	cat tx_elections_scrapers/sos/support/hs-2010_general.html | \
	  serialize_statewide | interpret_statewide > /dev/null
	cat tx_elections_scrapers/sos/support/rs-2012_rep_primary.htm | \
	  serialize_statewide | interpret_statewide > /dev/null
	cat tx_elections_scrapers/sos/support/hc-2014_special_sd28.html | \
	  serialize_county | interpret_county > /dev/null
	cat tx_elections_scrapers/sos/support/rc-2014_general_senate.html | \
	  serialize_county | interpret_county > /dev/null

# makes it easier to test setup.py's entry points
install:
	-pip uninstall $(APP) --yes
	pip install .

# Release Instructions:
#
# 1. bump version number at the top of this file
# 2. `make release`
#
# If this doesn't work, make sure you have wheels installed:
#     pip install wheel
release: clean
	@sed -i -r /version/s/[0-9.]+/$(VERSION)/ setup.py
	@git commit -am "bump version to v$(VERSION)"
	@git tag v$(VERSION)
	python setup.py sdist bdist_wheel upload
