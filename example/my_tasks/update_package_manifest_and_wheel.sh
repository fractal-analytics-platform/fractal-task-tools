#!/bin/bash

set -eu

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
python -m pip install -e ".[dev]"
python -m pip install -e "../.."
fractal-manifest create --package my-tasks
python -m build
deactivate
