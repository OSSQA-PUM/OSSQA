#!/bin/bash

# Generate coverage data
coverage run --source=main -m pytest -v /app/main/tests && coverage report -m

# Save exit code, so GitHub Actions interprets test results correct
EXIT_CODE=$?

# Redirect all fun-coverage output to a file,
# so it can be extracted via 'docker cp'
fun-coverage > .coverage.function 2>&1

exit $EXIT_CODE
