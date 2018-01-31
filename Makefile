TEST_CMD = nosetests -w ./tests --no-byte-compile

.PHONY: all test clean clean-build clean-pyc

all: clean test

test:
	$(TEST_CMD)

clean: clean-build clean-pyc

clean-build:
	rm -rf build
	rm -rf dist
	rm -rf vulnscanner.egg-info

clean-pyc:
	find . -type d -name '__pycache__' -exec rm -rf {} \;
	find . -type f -name '*.pyc' -exec rm -f {} \;
