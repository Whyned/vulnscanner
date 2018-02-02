TEST_CMD = nosetests -w ./tests --no-byte-compile
COVERAGE_CMD = nosetests --with-coverage --cover-package=vulnscanner --cover-erase --cover-inclusive --cover-html --cover-html-dir=./coverage

.PHONY: all test clean clean-build clean-pyc coverage

all: clean coverage

test:
	$(TEST_CMD)

clean: clean-build clean-pyc

clean-build:
	rm -rf build
	rm -rf dist
	rm -rf vulnscanner.egg-info
	rm -rf coverage

clean-pyc:
	find . -type d -name '__pycache__' -exec rm -rf {} 2>&1 /dev/null \;
	find . -type f -name '*.pyc' -exec rm -f {} 2>&1 /dev/null \;

coverage:
	$(COVERAGE_CMD)
