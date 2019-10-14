#!/bin/bash
# Install the package, force a quickstart, and build the site

sudo python setup.py install
ginpar-quickstart --force
ginpar