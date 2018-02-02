[![Build Status](https://travis-ci.org/Whyned/vulnscanner.svg?branch=master)](https://travis-ci.org/Whyned/vulnscanner)
[![Coverage Status](https://coveralls.io/repos/github/Whyned/vulnscanner/badge.svg?branch=master)](https://coveralls.io/github/Whyned/vulnscanner?branch=master)
# VulnScanner
A python3 vulnscanner with the goal to have an configurable, easy to hack and performant multi purpose vulnerability scanner.

## Introduction
Currently this is WIP, but for the moment already random port scanning works.
You can test it by executing `python3 -m vulnscanner`. To change ports to scan for, timeout etc have a look at `vulnscanner/__main__.py`

## Development
We use a Makefile to run different build scripts, so you need to have GNU Make installed.
We currently depend on the nose and coverage python modules, to install them, you can simply run `pip install -r requirements-dev.txt`. Make sure pip defaults to your python3 pip.

## Available make rules
- Run tests with `make test`
- Run tests with coverage with `make coverage`
- Clean with `make clean`

