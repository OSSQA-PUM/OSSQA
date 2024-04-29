#!/bin/bash

# Start test server (used in integration tests)
python src/test_backend_main.py > /dev/null 2>&1 &
BACKEND_PID=$!
sleep 1 # Ensure the test server starts before running the tests

coverage run --source src -m pytest -v src/tests/main/integration

# Kill test server
kill $BACKEND_PID
