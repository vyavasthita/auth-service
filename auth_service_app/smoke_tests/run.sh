#!/bin/bash

# SUMMARY:
# This script runs the Auth Service smoke tests using pytest.
# - Ensures any failure in the pipeline is detected (set -o pipefail).
# - Creates the output directory for logs.
# - Runs pytest with verbose output, logging to both console and /app/output/test_log.txt.
# - Captures the exit code of pytest (not tee) and exits with that code.
# - Prints the exit code for visibility.

set -o pipefail
echo "Running Smoke Tests for Auth Service..."

mkdir -p /app/output

# Run pytest with verbose output and log output to both console and file.
pytest -vvv | tee /app/output/test_log.txt

# Capture the exit code of tee (since PIPESTATUS is not available in sh)
exit_code=$?

echo "Smoke Tests completed with exit code $exit_code"
exit $exit_code