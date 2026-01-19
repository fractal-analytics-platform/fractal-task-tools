#!/bin/bash

set -eu

# Create a python venv
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Install tasks package in a venv
./venv/bin/python -m pip install -e "."

# Install the current version of fractal-task-tools
./venv/bin/python -m pip install -e ".."

# Create manifest
./venv/bin/fractal-manifest create --package example-tasks

# Cleanup
rm -r venv
