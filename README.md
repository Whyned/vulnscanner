# VulnScanner
A python3 vulnscanner with the goal to have an configurable, easy to hack and performant multi purpose vulnerability scanner.

# Introduction
Currently this is WIP, but for the moment already random port scanning works.
You can test it by executing `python3 -m vulnscanner`. To change ports to scan for, timeout etc have a look at `vulnscanner/__main__.py`

# Development
Needed python modules:
- nosetests
- coverage
Others:
- GNU make

## Available make rules
- Run tests with `make test`
- Run tests with coverage with `make coverage`
- Clean with `make clean`

