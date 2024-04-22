#!/bin/bash

# Generate coverage data
coverage run -m pytest --verbose

# Save exit code, so GitHub Actions interprets test results correct
EXIT_CODE=$?

# Redirect all fun-coverage output to a file,
# so it can be extracted via 'docker cp'
fun-coverage > .coverage.function 2>&1

exit $EXIT_CODE
