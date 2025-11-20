#!/bin/bash

# Manufacturer Onboarding Script
# This script runs the gateway registration process in a loop with timing

# Configuration
MAX_ATTEMPTS=5
DELAY_BETWEEN_ATTEMPTS=5  # seconds
PYTHON_SCRIPT="src/python/onlyRegisterGateway.py"
PYTHON_WIPE_SCRIPT="src/python/onlyWipeGateway.py"

echo "=== Gateway Manufacturer Onboarding ==="
echo "Max attempts: $MAX_ATTEMPTS"
echo "Delay between attempts: ${DELAY_BETWEEN_ATTEMPTS}s"
echo "========================================"
echo ""

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python script not found at $PYTHON_SCRIPT"
    exit 1
fi


echo "Starting registration at $(date '+%Y-%m-%d %H:%M:%S.%3N')"

# Record start time in milliseconds
start_time=$(date +%s%3N)

# Run the registration script
python3 "$PYTHON_SCRIPT"
exit_code=$?

# Record end time in milliseconds
end_time=$(date +%s%3N)
duration=$((end_time - start_time))

echo "Registration completed in ${duration}ms"

# Check if registration was successful
if [ $exit_code -eq 1 ]; then
    echo "FAILED: Registration failed (exit code: $exit_code)"
    exit 1
else
    echo "SUCCESS: Gateway registered successfully!"
fi

python3 "$PYTHON_WIPE_SCRIPT"
exit_code=$?

if [ $exit_code -eq 1 ]; then
    echo "FAILED: Wipe failed (exit code: $exit_code)"
    exit 1
else
    echo "SUCCESS: Gateway wiped successfully!"
fi
exit 0
