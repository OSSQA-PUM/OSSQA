#!/bin/bash

# This script is made to run in the docker container, if you run it
# outside of docker it may not work

# Start test server (used in integration tests)
python test_backend_main.py > /dev/null 2>&1 &
BACKEND_PID=$!

# Generate coverage data
# (--source .) is needed to include all functions in fun-coverage
coverage run --source . -m pytest -v

# Save exit code, so GitHub Actions interprets test results correct
EXIT_CODE=$?

# Kill test server
kill $BACKEND_PID

# Redirect all fun-coverage output to a file,
# so it can be extracted via 'docker cp'
fun-coverage > .coverage.function 2>&1

exit $EXIT_CODE
