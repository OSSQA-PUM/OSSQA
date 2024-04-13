#!/bin/bash

# Generate coverage data
coverage run -m pytest --verbose

# Redirect all fun-coverage output to a file,
# so it can be extracted via 'docker cp'
fun-coverage > .coverage.function 2>&1
